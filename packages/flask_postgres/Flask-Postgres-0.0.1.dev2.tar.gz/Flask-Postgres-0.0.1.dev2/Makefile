.PHONY: install
install:
	pip install build -e .[tests]

.PHONY: clean
clean:
	python setup.py sdist clean --all
	rm -rf build/ dist/ *.egg-info/

.PHONY: build
build:
	python setup.py sdist build

.PHONY: publish
publish:
	python setup.py sdist upload

.PHONY: test
test:
	pytest
