#!/usr/bin/env python3
"""Reject leaked held-out outcome cohort selection and missing zero-positive campaigns."""
import importlib.util
from collections import Counter
from pathlib import Path

SCRIPT=Path(__file__).with_name("criteo_full_stream_delay_audit.py")
spec=importlib.util.spec_from_file_location("criteo_eval", SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def build_group(campaign, source_time, delay, idx):
    ts=source_time+idx
    ct=ts+delay
    event=(ts,ct,campaign)
    return [event,None,1,0,str(idx),ct]

groups={}
day=86400
for campaign in ("A","B"):
    for i in range(24):
        groups[(campaign,"train",i)]=build_group(campaign,2*day,1200,i)
for i in range(24):
    groups[("A","test",i)]=build_group("A",18*day,1200,i)
# B meets train-positive support and test-impression threshold but has ZERO held-out positives.
# C has test impressions but no training positives, should be excluded.
exp_train=Counter({"A":5000,"B":5000})
exp_test=Counter({"A":1700,"B":1400,"C":1600})
out=mod.ipw_rate_diagnostic(groups,exp_train,exp_test)
assert sorted(out.keys())==["259200","3600","86400"],out.keys()
for w, x in out.items():
    assert x["status"]=="EXECUTED",(w,x)
    assert x["included_campaigns"]==2,(w,x)
    assert x["included_campaigns_with_zero_test_events"]==1,(w,x)
    assert x["included_test_exposures"]==3100,(w,x)
    assert x["actual_within_H_conversion_events"]==24,(w,x)
    assert x["early_events"]==24,(w,x)
    assert x["eligibility_rule"].endswith("no test-outcome selection")
    assert abs(x["per_campaign_absolute_event_rate_error_campaign"])<1e-10,(w,x)
print("PASS: train-supported zero-test-positive campaign included; unsupported C excluded; all 3 windows",flush=True)
