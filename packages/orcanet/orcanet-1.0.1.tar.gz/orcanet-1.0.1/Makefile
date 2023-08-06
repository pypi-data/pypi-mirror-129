PKGNAME=orcanet
ALLNAMES = $(PKGNAME)
ALLNAMES += orcanet_contrib
ALLNAMES += examples

all: install

install:
	pip install .

install-dev: dependencies
	pip install -e .

test:
	py.test $(PKGNAME)

retest:
	py.test $(PKGNAME) --last-failed

test-cov:
	py.test --cov ./ --cov-report term-missing --cov-report xml:reports/coverage.xml --cov-report html:reports/coverage $(ALLNAMES)

black:
	black orcanet

black-check:
	black --check orcanet

dependencies:
	pip install -Ur requirements.txt
	pip install -Ur requirements_dev.txt

.PHONY: all install install-dev test retest test-cov black black-check dependencies
