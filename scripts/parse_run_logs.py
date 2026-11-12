"""Collect the quantities that the pipeline prints (rather than writes to CSV) from the per-seed
run logs: smoothness sweep, embedding drift, transition/stability table and block bootstrap.

Usage:  python scripts/parse_run_logs.py [results_dir] [out_dir]
Reads   results/seed*/run_log.txt
Writes  <out_dir>/{lambda_sweep_long,stability_long,d7_long,bootstrap_long}.csv
"""
import re, sys
from pathlib import Path
import pandas as pd

RES = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else RES / "aggregated")
OUT.mkdir(parents=True, exist_ok=True)
seeds = sorted(int(p.name[4:]) for p in RES.glob("seed*") if (p / "run_log.txt").exists())
log = {k: (RES / f"seed{k}" / "run_log.txt").read_text() for k in seeds}

lam, stab, d7, boot = [], [], [], []
for k, t in log.items():
    for m in re.finditer(r"Lambda sensitivity, (\w+) @ (\d+)h ===\n(.*?)\nInterpretation", t, re.S):
        for l in m.group(3).splitlines()[1:]:
            p = l.split()
            if len(p) == 3:
                lam.append(dict(seed=k, dataset=m.group(1), resolution_h=int(m.group(2)),
                                lam=float(p[0]), persistence=float(p[1]), silhouette=float(p[2])))
    for m in re.finditer(r"=== Stability, (\w+) @ (\d+)h ===\n(.*?)(?=\n\n===|\Z)", t, re.S):
        for l in m.group(3).splitlines()[1:]:
            p = l.split()
            if len(p) == 3:
                stab.append(dict(seed=k, ds=m.group(1), res=int(m.group(2)), rep=p[0],
                                 drift=float(p[1]), sd=float(p[2])))
    for m in re.finditer(r"=== D7 transition/stability usefulness: (\w+) @ (\d+)h ===\n(.*?)(?=\n\n===|\n*\Z)", t, re.S):
        for l in m.group(3).splitlines()[1:]:
            mm = re.match(r"\s*(.+?)\s{2,}([\d.eE+-]+)\s+(True|False)\s+(\d+)\s+([\d.eE+-]+)\s+([\d.eE+-]+|NaN)\s*$", l)
            if mm:
                d7.append(dict(seed=k, ds=m.group(1), res=int(m.group(2)), rep=mm.group(1),
                               cps=int(mm.group(4)), drift=float(mm.group(5)), recall=mm.group(6)))
    for m in re.finditer(r"(\w+) @ (\d+)h bootstrap Silhouette 95% CI: (\{.*?\})", t):
        boot.append(dict(seed=k, ds=m.group(1), res=int(m.group(2)), **eval(m.group(3), {"__builtins__": {}}, {"nan": float("nan")})))

for name, rows in [("lambda_sweep_long", lam), ("stability_long", stab), ("d7_long", d7), ("bootstrap_long", boot)]:
    pd.DataFrame(rows).to_csv(OUT / f"{name}.csv", index=False)
    print(f"{name}: {len(rows)} rows")
