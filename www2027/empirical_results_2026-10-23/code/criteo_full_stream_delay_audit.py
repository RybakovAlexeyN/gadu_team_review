#!/usr/bin/env python3
"""Source-grounded Criteo observational validation of the GADU delay correction.

This is NOT offline policy/regret evaluation; the Criteo archive does not
include the randomized continuum-family actions/propensities required for it.

Input: original Criteo Attribution gzip TSV stream, 30 days of served ads.
Unit for the delay diagnostic: unique physical conversion_id with exactly
one chosen associated exposure (attributed-last-touch if available, else last-touch).
Estimand: P(impression-to-conversion lag <= w | lag <= H) among conversions
with an exposure having complete H-window follow-up in this archive.
This is NOT the unknown unconditional F(w) assumed in the paper.

One-pass, low-memory, Python stdlib only.
"""
import argparse
import csv
import gzip
import io
import json
import math
import os
import random
import sys
import time
from collections import Counter, defaultdict
from urllib.request import Request, urlopen

DEFAULT_URL = (
    "https://huggingface.co/datasets/criteo/criteo-attribution-dataset/"
    "resolve/904188a63cbad78bee43cd26ff5ee4ac77903986/criteo_attribution_dataset.tsv.gz?download=true"
)
FIELDS = [
    "timestamp","uid","campaign","conversion","conversion_timestamp",
    "conversion_id","attribution","click","click_pos","click_nb","cost",
    "cpo","time_since_last_click","cat1","cat2","cat3","cat4","cat5",
    "cat6","cat7","cat8","cat9"
]
DAY = 86400

def open_rows(path):
    if path.startswith(("https://", "http://")):
        response = urlopen(Request(path, headers={"User-Agent":"gadu-research-realdata/1.0"}), timeout=90)
        stream = gzip.GzipFile(fileobj=response) if ".gz" in path else response
        fh = io.TextIOWrapper(stream, encoding="utf-8", newline="")
    elif path.endswith(".gz"):
        fh = gzip.open(path, "rt", encoding="utf-8", newline="")
    else:
        fh = open(path, "r", encoding="utf-8", newline="")
    reader = csv.reader(fh, delimiter="\t")
    first = next(reader)
    if first[:3] == ["timestamp","uid","campaign"]:
        names = first
    else:
        names = FIELDS
        yield dict(zip(names,first))
    for raw in reader:
        if len(raw) != len(names):
            raise ValueError("Field count mismatch %s vs %s" % (len(raw),len(names)))
        yield dict(zip(names,raw))

def parse_log(input_path, max_rows):
    best = {}  # (uid, conversion_id, conversion_timestamp) -> linked source choices
    raw_cid_identity = {}  # audit reuse of anonymized conversion ID across users or event times
    train_exposures = Counter()
    test_exposures = Counter()
    total = 0
    positive_links = 0
    invalid_positive = 0
    max_ts = 0
    source_neg_delay = 0
    observed_attr_links = 0
    cross_user_ids = set()
    different_conversion_time_ids = set()
    start = time.monotonic()
    for row in open_rows(input_path):
        total += 1
        ts = int(row["timestamp"])
        if ts > max_ts: max_ts = ts
        if ts < 10*DAY:
            train_exposures[row["campaign"]] += 1
        elif 17*DAY <= ts < 23*DAY:
            test_exposures[row["campaign"]] += 1
        if row["conversion"] == "1":
            cid = row["conversion_id"]
            ct = int(row["conversion_timestamp"])
            if cid in ("-1","") or ct < ts:
                invalid_positive += 1
                source_neg_delay += int(ct < ts)
            else:
                positive_links += 1
                attr = int(row["attribution"])
                observed_attr_links += int(attr == 1)
                event = (ts, ct, row["campaign"])
                orig_identity = raw_cid_identity.get(cid)
                if orig_identity is None:
                    raw_cid_identity[cid] = (row["uid"], ct)
                else:
                    if orig_identity[0] != row["uid"]: cross_user_ids.add(cid)
                    if orig_identity[1] != ct: different_conversion_time_ids.add(cid)
                key = (row["uid"], cid, ct)
                old = best.get(key)
                if old is None:
                    best[key] = [event, event if attr == 1 else None, 1, int(attr == 1), row["uid"], ct]
                else:
                    old[2] += 1
                    old[3] += int(attr == 1)
                    if ts > old[0][0]: old[0] = event
                    if attr == 1 and (old[1] is None or ts > old[1][0]): old[1] = event
        if max_rows and total >= max_rows: break
        if total % 1000000 == 0:
            print("PROGRESS rows=%d physical_conversion_ids=%d minutes=%.2f"
                  % (total, len(best),(time.monotonic()-start)/60), flush=True)
    meta={
        "input": input_path,
        "impressions":total,
        "positive_source_links":positive_links,
        "distinct_raw_conversion_ids":len(raw_cid_identity),
        "distinct_conversion_event_keys":len(best),
        "distinct_conversion_ids":len(best),
        "duplicate_source_links":positive_links-len(best),
        "ids_with_multiple_links":sum(int(v[2]>1) for v in best.values()),
        "attributed_positive_source_links":observed_attr_links,
        "ids_with_attribution_one":sum(int(v[1] is not None) for v in best.values()),
        "invalid_positive":invalid_positive,
        "conversion_ids_crossing_uids":len(cross_user_ids),
        "grouping_key":["uid","conversion_id","conversion_timestamp"],
        "conversion_ids_crossing_timestamps":len(different_conversion_time_ids),
        "negative_impression_to_conversion_lags":source_neg_delay,
        "last_impression_timestamp":max_ts,
        "elapsed_parse_seconds":round(time.monotonic()-start,2),
    }
    return best,meta,train_exposures,test_exposures

def loss_report(train, test, windows, prior, meta, attribution_mode):
    H=windows[-1]
    cutoff=int(0.55*meta["last_impression_timestamp"])
    train_end=cutoff-H
    test_end=meta["last_impression_timestamp"]-H
    out={
        "attribution_choice":attribution_mode,
        "horizon_H_seconds":H,
        "train_source_end":train_end,
        "test_source_start":cutoff,
        "test_source_end":test_end,
        "embargo_seconds":H,
        "train_positive_events_within_H":len(train),
        "test_positive_events_within_H":len(test),
        "excluded_due_to_unmatured_or_other":meta["distinct_conversion_ids"]-len(train)-len(test),
        "campaigns_in_train":len(set(x[0] for x in train)),
        "campaigns_in_test":len(set(x[0] for x in test)),
        "windows":{},
    }
    for w in windows[:-1]:
        global_n=len(train)
        if global_n < 50 or len(test)<50:
            out["windows"][str(w)]={"status":"INSUFFICIENT_MATURE_POSITIVE_EVENTS"}
            continue
        pool=sum(int(lag<=w) for _,lag in train)/global_n
        by_g=defaultdict(lambda:[0,0])
        for g,lag in train:
            by_g[g][0]+=int(lag<=w);by_g[g][1]+=1
        sums=defaultdict(lambda:[0.0,0.0,0.0,0])
        early=0
        for g,lag in test:
            y=int(lag<=w);early+=y
            e,n=by_g[g]
            pg=(e+prior*pool)/(n+prior)
            # pairwise outcome logloss/brier
            sums[g][0]+=(y-pool)**2
            sums[g][1]+=(y-pg)**2
            sums[g][2]+= (1 if y else 0)/max(pool,1e-9)
            sums[g][3]+=1
        ntest=len(test)
        bp=sum(x[0] for x in sums.values())/ntest
        bg=sum(x[1] for x in sums.values())/ntest
        # Cluster bootstrap by campaign, not conversion row:
        rng=random.Random(20261023+w)
        gids=list(sums)
        improvements=[]
        for _ in range(300):
            drawn=(sums[gids[rng.randrange(len(gids))]] for __ in gids)
            vals=list(drawn)
            n=sum(x[3] for x in vals)
            improvements.append(sum(x[0]-x[1] for x in vals)/n)
        improvements.sort()
        def ci_index(frac): return improvements[int(frac*(len(improvements)-1))]
        trained_50=[(g,e/n,n) for g,(e,n) in by_g.items() if n>=50]
        out["windows"][str(w)]={
            "status":"EXECUTED",
            "training_pool_conditional_cdf_q_given_H":pool,
            "test_actual_conditional_cdf_q_given_H":early/ntest,
            "test_brier_pool":bp,
            "test_brier_campaign_shrunk":bg,
            "campaign_minus_pool_brier_improvement":bp-bg,
            "campaign_cluster_bootstrap_95_interval":[ci_index(.025),ci_index(.975)],
            "test_events":ntest,
            "train_campaigns_at_least_50_positives":len(trained_50),
            "campaign_q_range_at_n_ge_50":(
                [min(x[1] for x in trained_50),max(x[1] for x in trained_50)]
                if trained_50 else None
            ),
            "unseen_test_campaign_count":sum(int(g not in by_g) for g in sums),
            "caution":"Calibration of delay conditional on observed conversion within H; not GADU policy regret or causal uplift."
        }
    return out

def create_cohorts(groups, endtime, H, prefer_attribution):
    cutoff=int(.55*endtime)
    train_end=cutoff-H
    test_end=endtime-H
    train,test=[],[]
    for last,att,*_ in groups.values():
        ts,ct,camp=(att if prefer_attribution and att is not None else last)
        delay=ct-ts
        if delay<0 or delay>H:
            continue
        if ts<=train_end:
            train.append((camp,delay))
        elif cutoff<=ts<=test_end:
            test.append((camp,delay))
    return train,test


def ipw_rate_diagnostic(groups, exp_train, exp_test, H=7*DAY, prior=50.0):
    """Real-data retrospective count correction: N_early/q_est versus N_within_H.

    This is a source-linked *event-count* diagnostic, not the Bernoulli per-impression
    reward or an off-policy value estimate of an unobserved GADU action.
    Intervals are campaign-cluster descriptive bootstrap, not causal uncertainty.
    """
    train_H=Counter();test_H=Counter()
    results={}
    picked=[]
    for last,att,*_ in groups.values():
        ts,ct,camp=(att if att is not None else last)
        d=ct-ts
        if not 0 <= d <= H:
            continue
        if 0 <= ts < 10*DAY:
            picked.append(("train",camp,d))
            train_H[camp]+=1
        elif 17*DAY <=ts<23*DAY:
            picked.append(("test",camp,d))
            test_H[camp]+=1
    for w in (3600, DAY, 3*DAY):
        trE=Counter();teE=Counter()
        for split,g,d in picked:
            if d<=w:
                (trE if split=="train" else teE)[g]+=1
        pool=sum(trE.values())/max(1,sum(train_H.values()))
        rec=[]
        for g,ntrue in test_H.items():
            ntrain=train_H[g]
            nexposure=exp_test[g]
            if ntrain<20 or ntrue<20 or nexposure<1000:
                continue
            qc=(trE[g]+prior*pool)/(ntrain+prior)
            pred_pool=teE[g]/max(pool,1e-12)
            pred_grp=teE[g]/max(qc,1e-12)
            rec.append((g,ntrue,nexposure,teE[g],pred_pool,pred_grp))
        if not rec:
            results[str(w)]={"status":"INSUFFICIENT_GROUP_SUPPORT"}
            continue
        actual=sum(x[1] for x in rec)
        est_pool=sum(x[4] for x in rec)
        est_group=sum(x[5] for x in rec)
        exposure_count=sum(x[2] for x in rec)
        # Weighted MAE of per-impression event-rate error (not an unbiased policy value).
        abs_pool=sum(abs(x[4]-x[1]) for x in rec)/exposure_count
        abs_group=sum(abs(x[5]-x[1]) for x in rec)/exposure_count
        rng=random.Random(2026102300+w)
        improvements=[]
        for _ in range(300):
            cells=[rec[rng.randrange(len(rec))] for __ in range(len(rec))]
            denom=sum(x[2] for x in cells)
            imp=sum(abs(x[4]-x[1])-abs(x[5]-x[1]) for x in cells)/denom
            improvements.append(imp)
        improvements.sort()
        results[str(w)]={
            "status":"EXECUTED",
            "mature_train_event_count":sum(train_H.values()),
            "mature_test_event_count":sum(test_H.values()),
            "included_campaigns":len(rec),
            "included_test_exposures":exposure_count,
            "actual_within_H_conversion_events":actual,
            "early_events":sum(x[3] for x in rec),
            "estimated_events_pooled_q":est_pool,
            "estimated_events_campaign_shrunk_q":est_group,
            "aggregate_relative_bias_pooled":(est_pool-actual)/actual,
            "aggregate_relative_bias_campaign":(est_group-actual)/actual,
            "per_campaign_absolute_event_rate_error_pooled":abs_pool,
            "per_campaign_absolute_event_rate_error_campaign":abs_group,
            "event_rate_abs_error_improvement":abs_pool-abs_group,
            "campaign_cluster_bootstrap_95_interval":[improvements[7],improvements[292]],
            "warning":"Observational source-linked event count correction, not original GADU Bernoulli/no-interference/off-policy regret."
        }
    return results

def run(input_path,out_path,max_rows=0,H=7*DAY,ws=(3600,DAY,3*DAY),prior=50.0):
    if any(w>=H or w<=0 for w in ws): raise ValueError("require 0 < w < H")
    groups,meta,exp_train,exp_test=parse_log(input_path,max_rows)
    summary={"experiment":"Criteo full data delay-model audit, version 2",
        "estimand":"P(delay<=w | delay<=H, conversion within H, unique conversion_id, chosen source)",
        "source_data_not_randomized":True,"exposure_policy_GADU_tested":False,
        "real_data_meta":meta,"methods":{"H":H,"windows":list(ws),"shrinkage_prior":prior,
          "start_split_fraction":0.55,"embargo":H,
          "grouping":"campaign","source_pick":"last touch; sensitivity attributed=1 if available"}}
    for pref,mode in [(False,"latest_impression"),(True,"prefer_attribution_one_then_last_touch")]:
        train,test=create_cohorts(groups,meta["last_impression_timestamp"],H,pref)
        summary[mode]=loss_report(train,test,(*ws,H),prior,meta,mode)
    summary["ipw_rate_diagnostic"] = ipw_rate_diagnostic(groups,exp_train,exp_test,H,prior)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)),exist_ok=True)
    with open(out_path,"w",encoding="utf-8") as f: json.dump(summary,f,indent=2,sort_keys=True)
    print("RESULT_JSON_START",flush=True)
    # concise machine-readable excerpts in workflow log for immediate remote inspection
    print(json.dumps({"real_data_meta":meta,
      "main":summary["prefer_attribution_one_then_last_touch"]["windows"],
      "train_n":summary["prefer_attribution_one_then_last_touch"]["train_positive_events_within_H"],
      "test_n":summary["prefer_attribution_one_then_last_touch"]["test_positive_events_within_H"],
      "sensitivity_last_touch":summary["latest_impression"]["windows"],
      "ipw_rate_diagnostic":summary["ipw_rate_diagnostic"]},sort_keys=True),flush=True)
    print("RESULT_JSON_END",flush=True)
    print("WROTE",out_path,flush=True)
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",default=DEFAULT_URL)
    p.add_argument("--output",default="outputs/criteo_realdata_delay_v1.json")
    p.add_argument("--max-rows",type=int,default=0)
    args=p.parse_args()
    run(args.input,args.output,args.max_rows)
