check:
	black --check charybde
	isort --check-only charybde
	mypy charybde
	flake8 --count charybde
	pylint charybde

docs:
	sphinx-build -a -b html doc doc/_build/html

.PHONY: check docs
