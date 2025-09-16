VENV_DIR := ./venv
PIP := $(VENV_DIR)/bin/pip
PYTHON := $(VENV_DIR)/bin/python

# Installable service config
SERVICE_NAME := piscanner.client
SERVICE_FILE := $(SERVICE_NAME).service
INSTALL_DIR := /opt/piscanner
SYSTEMD_DIR := /etc/systemd/system

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup:  # Setup venv
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

.PHONY: dev-setup
dev-setup:  ## Setup Development
	$(PIP) install -r requirements-dev.txt
	$(PYTHON_VENV) install -e .

.PHONY: clean
clean:  ## Clean up build artifacts and caches
	rm -rf build/ dist/ .pytest_cache/
	rm -f $(SERVICE_FILE)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: build
build: clean  ## Build piscanner client
	$(PIP) install --upgrade build
	$(PYTHON) -m build

.PHONY: gen-service
gen-service:  ## Generate systemd service file
	@echo "Creating systemd service file $(SERVICE_FILE)..."
	@echo "[Unit]" > $@
	@echo "Description=Piscanner Service Client" >> $@
	@echo "After=network.target" >> $@
	@echo "Wants=network.target" >> $@
	@echo "" >> $@
	@echo "[Service]" >> $@
	@echo "Type=simple" >> $@
	@echo "User=root" >> $@
	@echo "ExecStart=$(PYTHON_VENV) -m piscanner" >> $@
	@echo "" >> $@
	@echo "[Install]" >> $@
	@echo "WantedBy=multi-user.target" >> $@

.PHONY: install
install: build  ## Install piscanner client
	$(PYTHON) -m build
	sudo mkdir -p $(INSTALL_DIR)
	sudo cp dist/*.whl $(INSTALL_DIR)
	sudo $(PYTHON) -m pip install $(INSTALL_DIR)/*.whl
	sudo cp $(SERVICE_FILE) $(SYSTEMD_DIR)
	sudo systemctl daemon-reload
	sudo systemctl enable $(SERVICE_NAME)
	sudo systemctl start $(SERVICE_NAME)

.PHONY: uninstall
uninstall:  ## Uninstall piscanner client
	sudo systemctl stop $(SERVICE_NAME)
	sudo systemctl disable $(SERVICE_NAME)
	sudo rm -f $(SYSTEMD_DIR)/$(SERVICE_FILE)
	sudo rm -rf $(INSTALL_DIR)

.PHONY: format
format:  ## Format code
	$(PYTHON) -m black .
	$(PYTHON) -m isort .
