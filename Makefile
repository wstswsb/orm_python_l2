lint:
	ruff check --fix .
	ruff format .
	mypy --strict .

up:
	docker compose up -d

down:
	docker compose down