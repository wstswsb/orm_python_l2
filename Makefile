lint:
	ruff format .
	ruff check --fix .
	mypy --strict .

up:
	docker compose up -d

down:
	docker compose down