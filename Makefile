run:
	docker compose unpause fefuschedule-api

stop:
	docker compose pause fefuschedule-api

update:
	cd api
	docker compose up -d --no-deps --build fefuschedule-api
	docker compose exec -w /api fefuschedule-api poetry run python -m alembic upgrade head

start:
	docker compose up --build -d
	docker compose exec -w /api fefuschedule-api poetry run python -m alembic upgrade head