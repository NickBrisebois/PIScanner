VENV_DIR := ./venv
PIP := $(VENV_DIR)/bin/pip
PYTHON := $(VENV_DIR)/bin/python

# Installable service config
SERVICE_NAME := piscanner.client
SERVICE_FILE := $(SERVICE_NAME).service
INSTALL_DIR := /opt/piscanner
SERVICE_VENV_DIR := $(INSTALL_DIR)/venv
SYSTEMD_DIR := /etc/systemd/system

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup:  # Setup venv
	# python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

.PHONY: dev-setup
dev-setup:  ## Setup Development
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) install -e .

.PHONY: dev-run
dev-run:  ## Run module piscanner.client (as root)
	sudo $(PYTHON) -m piscanner_client

.PHONY: clean
clean:  ## Clean up build artifacts and caches
	rm -rf build/ dist/ .pytest_cache/
	rm -f $(SERVICE_FILE)
	find . -path "./venv*" -prune -o -type f -name "*.pyc" -exec rm -f {} +
	find . -path "./venv*" -prune -o -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: build
build: clean  ## Build piscanner client
	$(PIP) install --upgrade build
	$(PYTHON) -m build

.PHONY: install
install:
	$(PIP) install -e .

.PHONY: format
format:  ## Format code
	$(PYTHON) -m black .
	$(PYTHON) -m isort .
