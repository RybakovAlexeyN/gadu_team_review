#!/usr/bin/env python3
"""Stdlib GitHub-facing MVP evidence/format verifier; NO bandit runs.
Usage: python code/verify_mvp_publication.py
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, re, math

ROOT = Path(__file__).resolve().parents[1]
read = lambda p: (ROOT / p).read_text(encoding='utf-8')
markdowns = ['README.md', 'CAPTIONS_METHODS_RESULTS.md', 'REVIEW_GATES.md']
for f in markdowns:
    s=read(f)
    assert '\\operatorname' not in s, (f, 'unsupported GitHub operatorname macro')
    assert s.count('$$') % 2 == 0, (f, 'unbalanced display math')
    assert s.count('```') % 2 == 0, (f, 'unbalanced code fences')
    for link in re.findall(r'!?(?:\[[^\]]*\])\(([^)]+)\)',s):
        target=link.split('#',1)[0]
        if not target or re.match(r'^(?:https?://|mailto:)',target) or target == 'E03_COAUTHOR_FIGURES_DATA.zip':
            continue
        assert (ROOT / target).exists(), (f, 'missing link',target)

frozen={}
with (ROOT / 'SHA256SUMS.txt').open() as f:
    for ln in f:
        h,rel=ln.rstrip('\n').split('  ',1)
        frozen[rel]=h
actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*')
        if p.is_file() and p.name not in {'SHA256SUMS.txt','E03_COAUTHOR_FIGURES_DATA.zip'}
        and '__pycache__' not in p.parts and 'regenerated' not in p.relative_to(ROOT).parts}
assert frozen==actual, ('manifest differs from actual files',set(frozen)^set(actual),
                        [p for p in frozen if p in actual and frozen[p]!=actual[p]])
# Runtime may generate local bytecode caches; verify only that the downloadable archive contains none.
if (ROOT / 'E03_COAUTHOR_FIGURES_DATA.zip').exists():
    with __import__('zipfile').ZipFile(ROOT / 'E03_COAUTHOR_FIGURES_DATA.zip') as z:
        assert not any('__pycache__' in x or x.endswith(('.pyc','.pyo')) for x in z.namelist())
for i in (1,2,3):
    name={1:'cumulative_regret',2:'stage_decomposition',3:'reward_functions'}[i]
    for ext in ('pdf','png','svg'):
        p=ROOT/f'figures/fig{i}_{name}.{ext}'
        assert p.stat().st_size>5000,(p,'too small')
        raw=p.read_bytes()
        assert (ext=='pdf' and raw[:4]==b'%PDF') or (ext=='png' and raw[:8]==b'\x89PNG\r\n\x1a\n') or (ext=='svg' and b'<svg' in raw[:1500]),p

with (ROOT/'data/e03_seed_runs.csv').open(newline='') as f: raw=list(csv.DictReader(f))
with (ROOT/'data/e03_per_seed_trajectory_checkpoints.csv').open(newline='') as f: pts=list(csv.DictReader(f))
with (ROOT/'data/table_e03_final.csv').open(newline='') as f: sums={r['scenario']:r for r in csv.DictReader(f)}
assert len(raw)==20 and len(pts)==2080 and sorted(Counter(r['world'] for r in raw).values())==[4,8,8]
assert len(sums)==3
for r in raw:
    eps=1e-5
    assert float(r['regret_search'])>float(r['cover_regret'])
    assert abs(float(r['paired_difference'])-(float(r['gadu_regret'])-float(r['cover_regret'])))<eps
    assert abs(sum(float(r[q]) for q in ('regret_search','regret_select','regret_continue'))-float(r['gadu_regret']))<eps
for name,r in sums.items():
    data=[x for x in raw if x['world']==name]
    assert int(r['n'])==len(data)
    for key,mean_key in [('gadu_regret','gadu_regret'),('cover_regret','cover_regret'),('regret_search','regret_search')]:
        mean=sum(float(x[key]) for x in data)/len(data)
        assert abs(mean-float(r[mean_key]))<eps,(name,key)
    assert 0<float(r['t95_lower'])<float(r['mean_delta'])<float(r['t95_upper'])
assert 'economic-rejection branch is structurally unreachable' in read('README.md')
assert 'acceptance branch is structurally unreachable' not in read('README.md')
print(f'PASS Markdown links/math, {len(actual)} file SHA256 checks, 3 PDF/SVG/PNG sets, '+
      f'{len(raw)} immutable seed rows, {len(pts)} checkpoints and scientific label sanity. '+
      'No new policy simulation.')
