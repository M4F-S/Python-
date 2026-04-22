PYTHON ?= python3
CONFIG ?= config.txt

.PHONY: install run debug clean lint lint-strict build

install:
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install build flake8 mypy

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

build:
	$(PYTHON) -m build

clean:
	rm -rf __pycache__ */__pycache__ */**/__pycache__
	rm -rf .mypy_cache .pytest_cache
	rm -rf build dist *.egg-info mazegen.egg-info
	rm -f maze.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
