.PHONY: all freeze check covercheck coverhtml

SRC=edt2ics

VENV=./venv
BINPREFIX=$(VENV)/bin/

PIP=$(BINPREFIX)pip

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

all: run

deps:
	$(BINPREFIX)pip install -qr requirements.txt

freeze: $(VENV)
	$(PIP) freeze >| requirements.txt

$(VENV):
	virtualenv $@

# Tests

check:
	$(BINPREFIX)python tests/test.py

check-versions:
	$(BINPREFIX)tox

covercheck:
	$(BINPREFIX)coverage run --source=$(SRC) tests/test.py
	$(BINPREFIX)coverage $(COVERAGE_REPORT)

coverhtml:
	@make COVERAGE_REPORT=html BINPREFIX=$(BINPREFIX) covercheck
	@echo '--> open htmlcov/index.html'

publish: deps check-versions
	$(BINPREFIX)python setup.py sdist upload
