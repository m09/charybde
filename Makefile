check:
	black --check charybde setup.py
	mypy charybde setup.py
	flake8 --count charybde setup.py

.PHONY: check
