#!/usr/bin/env python3
"""Public coauthor summary verifier; validates frozen aggregate CSVs, NOT full simulator parity."""
import argparse
import csv
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read_csv(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as h:
        return list(csv.DictReader(h))

def close(actual, expected, name, tol=1e-6):
    if not math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=tol):
        raise AssertionError(f"{name}: {actual} != {expected}")

def check():
    e17 = read_csv("E17_36cell_summary.csv")
    e20 = read_csv("E20_18cell_summary.csv")
    e21 = read_csv("E21_108case_certificate_feasibility.csv")
    assert len(e17) == 36 and len(e20) == 18 and len(e21) == 108
    assert len({(r["layout"], r["gap"], r["q"]) for r in e17}) == 36
    assert len({(r["layout"], r["gap"], r["q"]) for r in e20}) == 18
    assert len({(r["layout"], r["gap"], r["q"], r["seed"]) for r in e21}) == 108
    assert all(int(r["n_seeds"]) == 6 for r in e17)
    assert all(int(r["seeds"]) == 6 for r in e20)

    a17 = next(r for r in e17 if r["layout"]=="hetero_234" and r["gap"]=="large" and r["q"]=="0.75")
    for k,v in {"R_cert":2658.5799672825924, "R_noretire":6883.199720296428,
                "R_geo":1885.340290713107}.items():close(a17[k],v,"E17 "+k)
    assert int(a17["certificates"])==6

    a20 = next(r for r in e20 if r["layout"]=="hetero_234" and r["gap"]=="strong" and r["q"]=="0.75")
    for k,v in {"regret_adaptive_cert_geo_stage2":1605.7826622106734,
                "regret_adaptive_no_retire_geo_stage2":4151.586410379713,
                "regret_geo_ucb":1205.8335991288334,
                "stage1_regret":583.7169046570845}.items():close(a20[k],v,"E20 "+k)
    assert int(a20["cert_n"])==6
    assert sum(int(r["cert_n"]) for r in e20)==26
    # Regret win against direct geometric UCB attributable to retirement? In this
    # tested CSV, all mean wins occur in ZERO certificate cells.
    winning_cells = [r for r in e20 if float(r["regret_adaptive_cert_geo_stage2"]) <
       float(r["regret_geo_ucb"])]
    assert len(winning_cells)==5
    assert all(int(r["cert_n"])==0 for r in winning_cells)
    assert sum(1 for r in e20 if int(r["cert_n"])>0)==5

    feas = Counter()
    actual = Counter()
    for r in e21:
        gap = r["gap"]
        feas[gap] += r["population_feasible"].strip().lower() == "true"
        actual[gap] += r["actually_certified"].strip().lower() == "true"
    assert dict(feas) == {"strong":36,"moderate":36,"near_tie":0},feas
    assert dict(actual) == {"strong":26,"moderate":0,"near_tie":0},actual

    fig = (ROOT / "figures" / "e20_certification_vs_geometry.svg").read_text(encoding="utf-8")
    for required in ("1,205.8","1,605.8","4,151.6","20,000","six matched seeds"):
        assert required in fig,("Figure missing numeric/source label",required)

    print("PASS: exact original CSV rows E17=36 E20=18 E21=108; E20 verified no certified direct-geo wins; E21 feasibility; E20 SVG labels.")
    print("NOTE: numeric aggregate validator only; raw stochastic reruns and author GADU source parity are NOT established.")

if __name__ == "__main__":
    check()
