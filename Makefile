.PHONY: all freeze check covercheck coverhtml

SRC=edt2ics

VENV=./venv
BINUTILS=$(VENV)/bin

PIP=$(BINUTILS)/pip

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

freeze: $(VENV)
	$(PIP) freeze >| requirements.txt

$(VENV):
	virtualenv $@

# Tests

check:
	$(BINUTILS)/python tests/test.py

covercheck:
	$(BINUTILS)/coverage run --source=$(SRC) tests/test.py
	$(BINUTILS)/coverage $(COVERAGE_REPORT)

coverhtml:
	@make COVERAGE_REPORT=html covercheck
	@echo '--> open htmlcov/index.html'

publish: deps
	$(BINUTILS)/python setup.py sdist upload
