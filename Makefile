
format:
	isort .
	black .

check:
	mypy .

test:
	pytest -v
