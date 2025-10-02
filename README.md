# Riemann Publication Package

**Date:** 2025-10-02

This repository contains:
- Analytic proof framework (T1′–T4) in `analytic/` + `theorems/` (computation-independent).
- Weighted T2 bound implemented in `scripts/`, lambda figure in `outputs/`.
- T3 wave-packet appendix, dispersion companion paper.
- InterIA: impacts doc, TikZ triptyque, 1-page slide, CI workflow, schemas, Makefile.

## Build
- `make paper` --- main proof PDF (T1′–T4 + T3 appendix)
- `make frame-report` --- JSON report for weighted T2
- `make lambda-figure` --- lambda comparison PNG
- `make hr-ia-impacts` --- impacts IA/RH PDF
- `make robin-slide` --- 1-page slide
- `make triptyque-pdf` / `make triptyque-slide`
