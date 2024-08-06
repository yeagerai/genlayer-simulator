## Pre-requisites

### Window One
1. Launch the simulator

### Window Two
1. Set your virtual environment
2. pip install `pip install -r backend/database_handler/requirements.txt`
4. Update the "models" at `models.py` with your preferences
5. Set your current working directory to `backend/database_handler`
6. Run `alembic revision --autogenerate -m "migration name here"` to generate the migration file
7. Modify the migration file if needed
8. Apply the migration: we have different options here
   - [preferred] If using `docker-compose`, run `docker compose up database-migration --build`
   - Run `alembic upgrade head` to "manually" apply the migration

## Revert migrations
To revert the latest migration, run `alembic downgrade -1`

## Docs

- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
