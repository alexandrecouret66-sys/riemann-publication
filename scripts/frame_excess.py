#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Weighted frame excess bound for the prime-power grid Xi_A (subset of [-A, A]) with weights
w_{p,k} = log(p) / p^{k/2}. Implements:
  C_fr^{(w)}(A) >= g0 - Theta_w(A),
with g0 = hatphi(0) and
  Theta_w(A) = sup_alpha sum_{beta != alpha} sqrt(w_beta / w_alpha) * |hatphi(xi_alpha - xi_beta)|.
We use a smooth, even, compactly supported window: cosine^2 taper on [-A, A].
'''
import argparse, math, numpy as np
from pathlib import Path
import json

def cos2_taper_hat(t: float, A: float, alpha: float = 0.25) -> float:
    at = abs(t)
    if at > A: return 0.0
    plateau = (1.0 - alpha) * A
    if at <= plateau: return 1.0
    u = (at - plateau) / (alpha * A)
    u = max(0.0, min(1.0, u))
    c = math.cos(0.5 * math.pi * u)
    return float(c * c)

def primes_up_to(n: int):
    if n < 2: return []
    sieve = np.ones(n + 1, dtype=bool); sieve[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]: sieve[p*p::p] = False
    return list(np.flatnonzero(sieve))

def prime_power_grid_and_weights(A: float):
    Pmax = int(math.exp(A)) + 1
    ps = primes_up_to(Pmax)
    xis, ws = [], []
    for p in ps:
        lp = math.log(p)
        if lp <= 0: continue
        kmax = int(A / lp)
        for k in range(1, kmax + 1):
            xi = k * lp
            if 0.0 <= xi <= A:
                w = lp / (p ** (0.5 * k))
                xis.append(xi); ws.append(w)
    order = np.argsort(xis)
    return np.array([xis[i] for i in order], float), np.array([ws[i] for i in order], float)

def theta_w(A: float, alpha: float = 0.25):
    xis, ws = prime_power_grid_and_weights(A)
    if len(xis) == 0: return 0.0, 1.0, 0, 0.0
    g0 = 1.0
    x = xis; w = ws; n = len(x)
    diff = x.reshape(n,1) - x.reshape(1,n)
    vhat = np.vectorize(lambda tt: cos2_taper_hat(float(tt), A, alpha))
    hatphi = vhat(diff); np.fill_diagonal(hatphi, 0.0)
    sqrt_ratio = np.sqrt(w.reshape(1,n) / w.reshape(n,1))
    terms = sqrt_ratio * np.abs(hatphi)
    row_sums = terms.sum(axis=1)
    Theta = float(np.max(row_sums))
    return Theta, g0, n, float(x.max() if n>0 else 0.0)

def compute_cfr(A: float, alpha: float = 0.25):
    Theta, g0, n, xmax = theta_w(A, alpha=alpha)
    Cfr = max(0.0, g0 - Theta)
    return Cfr, Theta, g0, n, xmax

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--A", type=float, default=8.0, help="Bandwidth A")
    ap.add_argument("--alpha", type=float, default=0.25, help="Taper parameter alpha")
    ap.add_argument("--json", type=str, default="", help="Optional JSON output path")
    args = ap.parse_args()
    Cfr, Th, g0, n, xmax = compute_cfr(args.A, alpha=args.alpha)
    out = {"A": args.A, "alpha": args.alpha, "Cfr": Cfr, "Theta": Th, "g0": g0, "num_grid": n, "xmax": xmax}
    print(out)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(out, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
