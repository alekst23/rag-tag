# Define the path to the virtual environment
VENV := .venv

# Define the command to activate the virtual environment
ACTIVATE_VENV := . $(shell pwd)/$(VENV)/bin/activate

# Define the root directory of the project
PROJECT_ROOT := $(shell pwd)

test:
	@$(ACTIVATE_VENV) && PYTHONPATH=$(PROJECT_ROOT) pytest

test-llm:
	@$(ACTIVATE_VENV) && PYTHONPATH=$(PROJECT_ROOT) pytest tests/unit/backend/test_unit_llm.py
	@$(ACTIVATE_VENV) && PYTHONPATH=$(PROJECT_ROOT) pytest tests/int/backend/test_llm.py

test-ragtag:
	@$(ACTIVATE_VENV) && PYTHONPATH=$(PROJECT_ROOT) pytest tests/int/backend/test_ragtag.py
	
.PHONY: test