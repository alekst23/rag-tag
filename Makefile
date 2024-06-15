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

install:
	@echo "Installing RAG-TAG..."
	@pip install -e .

uninstall:
	@echo "Uninstalling RAG-TAG..."
	@pip uninstall -y ragtag

reinstall: uninstall install

status:
	@pip show ragtag
	@pip list | grep ragtag
	@python -c "import ragtag"