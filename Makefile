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
	rm -rf dist/
	rm -rf *.egg-info

debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
