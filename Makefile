PROJECT = project

run:
	python3 a_maze_ing.py config.txt

install:
	cd $(PROJECT) && poetry install

clean:
	rm -rf */__pycache__
	rm -rf __pycache__/
	rm -rf .mypy_cache

debug:
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict