# Convenience Makefile

PY ?= python
VENV ?= ~/.venvs/lesegenv

.PHONY: help install verify-data pipeline ablations figures clean

help:
	@echo "Targets:"
	@echo "  install        Install Python dependencies into $(VENV)"
	@echo "  verify-data    Check for SCP1219 files in data/raw/"
	@echo "  pipeline       Run full pipeline (qc→stats→figures)"
	@echo "  ablations      Run all 10 ablation experiments"
	@echo "  figures        Regenerate figures only"
	@echo "  clean          Remove processed data and results (keeps data/raw/)"

install:
	$(VENV)/bin/pip install -r requirements.txt

verify-data:
	$(PY) scripts/download_data.py --verify

pipeline:
	$(PY) scripts/run_pipeline.py --step all

ablations:
	$(PY) scripts/ablations/run_all_ablations.py

figures:
	$(PY) scripts/run_pipeline.py --step figures

clean:
	rm -rf data/processed/* results/intermediate/* results/figures/* results/tables/* results/ablations/*
