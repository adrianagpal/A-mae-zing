PROJECT = project

run:
	python3 a_maze_ing.py config.txt

install:
	pip install --upgrade pip setuptools wheel build
	pip install -e .

install-dev:
	pip install --upgrade pip setuptools wheel build
	pip install -e . flake8 mypy

build:
	python3 -m build --wheel

clean:
	rm -rf */__pycache__
	rm -rf __pycache__/
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf build/

pack
	pip install --upgrade pip setuptools wheel build
	pip install -e .
	python3 -m build --wheel
	
debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
