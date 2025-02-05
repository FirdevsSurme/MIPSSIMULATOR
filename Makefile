# Makefile for MIPS Simulator

# Python interpreter
PYTHON = python3

# Virtual environment
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP = $(VENV_BIN)/pip

# Source files
MAIN = mips_simulator.py
SOURCES = $(MAIN)

# Dependencies
REQUIREMENTS = requirements.txt

# Default target
.PHONY: all
all: venv run

# Create virtual environment
.PHONY: venv
venv:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip
	test -f $(REQUIREMENTS) || echo "tkinter" > $(REQUIREMENTS)
	$(VENV_PIP) install -r $(REQUIREMENTS)

# Run the application
.PHONY: run
run: venv
	$(VENV_PYTHON) $(MAIN)

# Clean build artifacts and virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV) __pycache__ *.pyc .pytest_cache

# Install dependencies
.PHONY: install
install: venv

# Run tests (if you add them in the future)
.PHONY: test
test: venv
	$(VENV_PYTHON) -m pytest tests/

# Format code using black (optional)
.PHONY: format
format: venv
	$(VENV_PIP) install black
	$(VENV_BIN)/black $(SOURCES)

# Check code style (optional)
.PHONY: lint
lint: venv
	$(VENV_PIP) install flake8
	$(VENV_BIN)/flake8 $(SOURCES)

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all      : Set up virtual environment and run the application"
	@echo "  venv     : Create virtual environment and install dependencies"
	@echo "  run      : Run the MIPS simulator"
	@echo "  clean    : Remove virtual environment and build artifacts"
	@echo "  install  : Install project dependencies"
	@echo "  test     : Run tests (needs to be implemented)"
	@echo "  format   : Format code using black"
	@echo "  lint     : Check code style using flake8"
	@echo "  help     : Show this help message"

#test codes
addi $t0, $zero, 5
addi $t1, $zero, 3
add $t2, $t0, $t1
sub $t3, $t0, $t1
sw $t2, 0($zero)
lw $t4, 0($zero)