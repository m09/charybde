check:
	black --check charybde
	mypy charybde
	flake8 --count charybde

.PHONY: check
