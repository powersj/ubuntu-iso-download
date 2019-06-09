PYTHON = python3
SETUP  := $(PYTHON) setup.py

.PHONY: clean install publish snap test venv

clean:
	$(SETUP) clean
	rm -f .coverage .eggs *.iso *.snap *.tar.bz2
	rm -rf build/ dist/ prime/ stage/ htmlcov/ venv/
	rm -rf *.egg-info .pytest_cache/ .tox/
	@find . -regex '.*\(__pycache__\|\.py[co]\)' -delete

install:
	$(SETUP) install

publish:
	rm -rf dist/
	$(SETUP) sdist
	twine check dist/ubuntu-iso-download-*.tar.gz
	twine upload dist/*

snap:
	snapcraft cleanbuild

test:
	$(SETUP) test
	tox

venv:
	$(PYTHON) -m virtualenv -p /usr/bin/$(PYTHON) venv
	venv/bin/pip install -Ur requirements.txt -Ur requirements-test.txt
	venv/bin/pip install twine
	@echo "Now run the following to activate the virtual env:"
	@echo ". venv/bin/activate"
