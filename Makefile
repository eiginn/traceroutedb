.PHONY: clean-pyc clean-build docs clean clean-deb

help:
	@echo "clean - remove all build, test, coverage, deb build, and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-deb - remove deb build artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "deb - deb package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test clean-deb

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-deb:
	rm -rf debian/debhelper-build-stamp \
	       debian/files \
	       debian/traceroutedb.debhelper.log \
	       debian/traceroutedb.postinst.debhelper \
	       debian/traceroutedb

lint:
	flake8 traceroutedb tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source traceroutedb setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/traceroutedb.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ traceroutedb
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

deb-prereq:
	sudo apt-get update
	sudo apt-get install dh-virtualenv debhelper devscripts python-all libffi-dev libpq-dev
	# sudo pip install make-deb

deb: clean
	dpkg-buildpackage -us -uc

dev-db:
	./sql/dev-db.sh
