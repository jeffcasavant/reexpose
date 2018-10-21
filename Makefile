.PHONY: all packages

all: run

run: install
	reexpose --config config.yaml

install:
	pip install .

install-dev:
	pip install.[dev]

packages: wheel source

wheel:
	mkdir -p build
	mkdir -p dist/wheel
	pip wheel --wheel-dir dist/wheel --build build .

source:
	python setup.py sdist
