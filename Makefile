# Convenience Makefile
#
# Override PY/VENV on the command line if needed, e.g.:
#   make install PY=py -3.12
#   make pipeline VENV=/path/to/existing/venv

PY ?= python3
VENV ?= .venv

VENV_BIN := $(VENV)/bin
ifeq ($(OS),Windows_NT)
VENV_BIN := $(VENV)/Scripts
endif
VENV_PY := $(VENV_BIN)/python

.PHONY: help venv install install-locked verify-data pipeline ablations figures test clean

help:
	@echo "Targets:"
	@echo "  venv           Create a local virtual environment at $(VENV)"
	@echo "  install        Create $(VENV) (if needed) and install dependencies into it"
	@echo "                 (from requirements.txt; harmonypy needs a C++ toolchain)"
	@echo "  install-locked Same, but from the pinned requirements.lock.txt snapshot"
	@echo "                 for exact, previously-verified-working versions"
	@echo "  verify-data    Check for SCP1219 files in data/raw/"
	@echo "  pipeline       Run full pipeline (qc→stats→figures)"
	@echo "  ablations      Run all 10 ablation experiments"
	@echo "  figures        Regenerate figures only"
	@echo "  test           Run the pytest suite"
	@echo "  clean          Remove processed data and results (keeps data/raw/)"

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements.txt

install-locked: venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements.lock.txt

verify-data:
	$(VENV_PY) scripts/download_data.py --verify

pipeline:
	$(VENV_PY) scripts/run_pipeline.py --step all

ablations:
	$(VENV_PY) scripts/ablations/run_all_ablations.py

figures:
	$(VENV_PY) scripts/run_pipeline.py --step figures

test:
	$(VENV_PY) -m pytest tests/ -v

clean:
	rm -rf data/processed/* results/intermediate/* results/figures/* results/tables/* results/ablations/*
