#!/usr/bin/env python3
"""Verify frozen E17/E20/E21 summaries, captions/figures, and export vector PDF + PNG.
Scientific scope: exploratory synthetic surrogates; DOES NOT rerun original GADU.
"""
from __future__ import annotations
import argparse
import csv
import math
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
KNOWN={
 "E17_36cell_summary.csv":("cca8fcbec48327e2d39a16dcdf96f5ef7d45725b",36),
 "E20_18cell_summary.csv":("c19ffe65b4822e216da4ba63f83f3126ccc5ab49",18),
 "E21_108case_certificate_feasibility.csv":("ebcf22a90d4c9a172f0049919d8217a68c2d84ce",108)
}
FIGS=("fig1_main_result_d234_regret","fig2_certification_map","fig3_stage1_adaptation","fig4_research_logic_diagram")

def read_csv(file):
    with (ROOT/"data"/file).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

def expect_near(val,goal,label):
    if not math.isclose(float(val),float(goal),rel_tol=0,abs_tol=1e-6):
        raise ValueError(f"{label}: {val} != {goal}")

def verify():
    for fn,(sha,n) in KNOWN.items():
        p=ROOT/"data"/fn
        got=subprocess.check_output(["git","hash-object",str(p)],text=True).strip()
        if got!=sha:raise ValueError(f"Git blob differs from frozen source: {fn}: {got}")
        if len(read_csv(fn))!=n:raise ValueError(f"Unexpected row count: {fn}")
    A=read_csv("E17_36cell_summary.csv")
    B=read_csv("E20_18cell_summary.csv")
    C=read_csv("E21_108case_certificate_feasibility.csv")
    D=read_csv("E18_E19_report_aggregates.csv")
    if len({(r["layout"],r["gap"],r["q"]) for r in A})!=36:raise ValueError("E17 duplicate cells")
    if len({(r["layout"],r["gap"],r["q"]) for r in B})!=18:raise ValueError("E20 duplicate cells")
    if len({(r["layout"],r["gap"],r["q"],r["seed"]) for r in C})!=108:raise ValueError("E21 duplicate seed-cells")
    if any(int(r["n_seeds"])!=6 for r in A):raise ValueError("E17 n_seeds")
    if any(int(r["seeds"])!=6 for r in B):raise ValueError("E20 seeds")
    main=next(r for r in B if (r["layout"],r["gap"],r["q"])==("hetero_234","strong","0.75"))
    geo=float(main["regret_geo_ucb"])
    cert=float(main["regret_adaptive_cert_geo_stage2"])
    no=float(main["regret_adaptive_no_retire_geo_stage2"])
    expect_near(no,4151.586410379713,"E20 no retirement")
    expect_near(cert,1605.7826622106734,"E20 retirement")
    expect_near(geo,1205.8335991288334,"E20 geo")
    expect_near((no-cert)/no*100,61.321227514476696,"E20 retirement percentage")
    expect_near(cert-geo,399.94906308184,"E20 staged-geo gap")
    if int(main["cert_n"])!=6 or sum(int(r["cert_n"]) for r in B)!=26: raise ValueError("E20 certificates")
    winning=[r for r in B if float(r["regret_adaptive_cert_geo_stage2"]) < float(r["regret_geo_ucb"])]
    if len(winning)!=5 or any(int(r["cert_n"])>0 for r in winning):raise ValueError("E20 win / certificate separation")
    if len([r for r in B if int(r["cert_n"])>0])!=5:raise ValueError("E20 certificate cell counts")
    def cert_sum(gap,q):return sum(int(r["certificates"]) for r in A if r["gap"]==gap and r["q"]==q)
    if cert_sum("large","0.75")!=36 or cert_sum("large","0.35")!=9:raise ValueError("E17 strong counts")
    if sum(int(r["certificates"]) for r in A if r["gap"]!="large")!=0:raise ValueError("E17 other counts")
    if sum(r["population_feasible"].lower()=="true" for r in C if r["gap"]=="strong")!=36:raise ValueError("E21 strong feasible")
    if sum(r["population_feasible"].lower()=="true" for r in C if r["gap"]=="moderate")!=36:raise ValueError("E21 moderate feasible")
    if sum(r["population_feasible"].lower()=="true" for r in C if r["gap"]=="near_tie")!=0:raise ValueError("E21 near-tie feasible")
    def value(exp,quantity,layout="all_layouts",gap="all_gaps",q="both"):
        r=next(x for x in D if (x["experiment"],x["layout"],x["gap"],x["q"],x["quantity"])==(exp,layout,gap,q,quantity))
        return float(r["value"])
    for what,expect in (
      ("stage1_best_family_mean_pulls",7140.2),
      ("stage1_inferior_family_d3_mean_pulls",26.5),
      ("stage1_inferior_family_d4_mean_pulls",33.3)
    ):
        expect_near(value("E18",what,"hetero_234","strong","0.75"),expect,what)
    expect_near(value("E18","observed_adaptive_certifications"),0,"E18 certificates")
    expect_near(value("E19","observed_adaptive_certifications"),21,"E19 certificates")
    for fig in FIGS:
        p=ROOT/"figures"/(fig+".svg")
        if not p.is_file():raise ValueError("Missing figure: "+fig)
        tree=ET.parse(p).getroot()
        if not tree.tag.endswith("svg"):raise ValueError("Not SVG: "+fig)
        if "viewBox" not in tree.attrib:raise ValueError("Missing SVG viewBox: "+fig)
        if len(p.read_bytes())<1000:raise ValueError("Suspiciously short figure: "+fig)
    # Non-causal wording is essential for figures 3 and 4.
    if b"NOT a paired" not in (ROOT/"figures"/"fig3_stage1_adaptation.svg").read_bytes() and b"NOT a paired" not in (ROOT/"FIGURE_GUIDE.md").read_bytes():
        raise ValueError("Unpaired E18/E19 warning missing")
    print("PASS: 3 frozen Git blob hashes, E17/E20/E21 tables, E18/E19 report aggregates, and four valid SVGs.")
    print("NOTE: this is an aggregated-result integrity audit, NOT a re-run of the author GADU-Cover algorithm.")

def export():
    try:
        import cairosvg
    except ImportError as ex:
        raise SystemExit("For PDF/PNG export: pip install cairosvg") from ex
    out=ROOT/"dist"/"figures"
    out.mkdir(parents=True,exist_ok=True)
    for figure in FIGS:
        data=(ROOT/"figures"/(figure+".svg")).read_bytes()
        # SVG stays the canonical editable vector source; rendered PDF is vector, PNG ~300 dpi or better at journal widths.
        cairosvg.svg2pdf(bytestring=data,write_to=str(out/(figure+".pdf")))
        cairosvg.svg2png(bytestring=data,write_to=str(out/(figure+".png")),output_width=3600)
        pdf=(out/(figure+".pdf")).read_bytes()
        png=(out/(figure+".png")).read_bytes()
        if not pdf.startswith(b"%PDF") or not png.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Rendered binary signature incorrect: "+figure)
        print(f"EXPORTED {figure}.pdf, {figure}.png")
    (out/"README.txt").write_text(
      "Four PDF + PNG figures. Canonical source SVG and frozen CSVs in GitHub branch. "
      "Exploratory surrogate results; NOT final-author GADU validation.\n",encoding="utf-8"
    )

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--export",action="store_true")
    args=ap.parse_args()
    verify()
    if args.export: export()
