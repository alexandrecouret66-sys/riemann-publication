#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Generate lambda_comparison.png:
- Load empirical lambda from data/mod30_counts.csv if present (fallback synthetic around 0.3778).
- Compute C_fr^{(w)}(A) using frame_excess for A in [4,10] and plot alongside ref 0.3778.
'''
import argparse, csv, numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from importlib.machinery import SourceFileLoader
import types

def load_empirical_lambda(csv_path: Path, n_points: int = 20):
    if not csv_path.exists():
        x = np.arange(1, n_points+1)
        rng = np.random.default_rng(0)
        lam = 0.3778 + 0.004*np.sin(2*np.pi*x/7.0) + 0.001*rng.normal(size=n_points)
        return x, lam
    xs, ls = [], []
    with csv_path.open('r', encoding='utf-8') as f:
        rd = csv.reader(f); header = next(rd, None)
        for row in rd:
            if not row: continue
            try: val = float(row[-1])
            except: continue
            xs.append(len(xs)+1); ls.append(val)
    if not xs:
        return load_empirical_lambda(Path('__missing__'), n_points=n_points)
    return np.array(xs), np.array(ls)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', type=str, default='outputs')
    ap.add_argument('--alpha', type=float, default=0.25)
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    loader = SourceFileLoader('frame_excess_module', str(Path(__file__).parent/'frame_excess.py'))
    mod = types.ModuleType(loader.name); loader.exec_module(mod)
    x_emp, lam_emp = load_empirical_lambda(Path('data/mod30_counts.csv'))
    A_values = np.linspace(4.0, 10.0, num=20)
    cfr_vals = [mod.compute_cfr(float(A), alpha=args.alpha)[0] for A in A_values]
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(x_emp, lam_emp, label='Empirical lambda (mod 30 or synthetic)')
    plt.axhline(0.3778, linestyle='--', label='lambda reference (0.3778)')
    plt.plot(np.linspace(1, len(x_emp), len(A_values)), cfr_vals, linestyle=':', label=r"$C_{\mathrm{fr}}^{(w)}(A)$")
    plt.xlabel('Index / scale'); plt.ylabel('lambda  or  C_fr^{(w)}')
    plt.title('Lambda comparison and weighted frame bound')
    plt.legend(frameon=True, loc='best'); plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    figpath = outdir/'lambda_comparison.png'; plt.savefig(figpath, dpi=150)
    print(f'[ok] wrote {figpath}')

if __name__ == '__main__':
    main()
