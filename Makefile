.PHONY: all packages

all: run

run: install
	reexpose --config config.yaml

install:
	pip install .

install-dev:
	pip install .[dev]

packages: wheel source

wheel: install-dev
	mkdir -p build
	mkdir -p dist
	pip wheel --wheel-dir dist --build build .

source: install-dev
	python setup.py sdist

upload: clean install-dev packages
	twine upload dist/ReExpose*

clean:
	rm -rf dist
	rm -rf build
