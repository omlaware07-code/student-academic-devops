#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p reports
python -m pytest -v --cov=app --junitxml=reports/test-results.xml tests/
echo "Tests finished. To start: source .venv/bin/activate && python run.py"
