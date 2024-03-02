#!/bin/bash
set -e
cd /code
echo "Running pytest"
pdm run pytest
echo "Running black"
pdm run black ./ --check
echo running "mypy"
pdm run mypy . || true
