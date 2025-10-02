.PHONY: paper frame-report lambda-figure hr-ia-impacts robin-slide triptyque-pdf triptyque-slide hp-test-all hp-ci-gates-dev hp-ci-gates-staging hp-ci-gates-prod
paper:
	cd analytic && latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex || true
frame-report:
	@python3 scripts/frame_excess.py --A 8.0 --json outputs/frame_report_A8.json
	@echo "OK: outputs/frame_report_A8.json"
lambda-figure:
	@python3 scripts/generate_lambda_comparison.py --outdir outputs
	@echo "OK: outputs/lambda_comparison.png"
hr-ia-impacts:
	@latexmk -pdf -halt-on-error -interaction=nonstopmode -outdir=docs docs/impacts_IA_HR.tex
	@echo "OK: docs/impacts_IA_HR.pdf"
robin-slide:
	@latexmk -pdf -halt-on-error -interaction=nonstopmode -outdir=slides slides/robin_interia_beamer.tex
	@echo "OK: slides/robin_interia_beamer.pdf"
triptyque-pdf:
	@latexmk -pdf -silent -halt-on-error -interaction=nonstopmode -outdir=docs docs/fig_triptyque.tex
	@echo "✅ docs/fig_triptyque.pdf"
triptyque-slide:  triptyque-pdf
	@latexmk -pdf -silent -halt-on-error -interaction=nonstopmode -outdir=slides slides/frag_triptyque.tex
	@echo "✅ slides/frag_triptyque.pdf"
hp-test-all:
	@echo "Running local test suite placeholders (adapt scripts in tools/)"
	@echo "OK: hp-test-all"
hp-ci-gates-dev:
	@echo "DEV gates placeholder (plug tools/ci_gates.py)"
hp-ci-gates-staging:
	@echo "STAGING gates placeholder (plug tools/ci_gates.py)"
hp-ci-gates-prod:
	@echo "PROD gates placeholder (plug tools/ci_gates.py)"
