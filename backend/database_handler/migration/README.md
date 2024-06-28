## Pre-requisites

1. set your virtual environment
1. `pip install -r requirements.txt`

## User guide

1. Change the `model`
1. Set your current working directory to `backend/database_handler`
1. Run `alembic revision --autogenerate -m "migration name here"` to generate the migration file
1. Modify the migration file if needed
1. Apply the migration: we have different options here
   - [preferred] If using `docker-compose`, run `docker-compose up database-migration --build`
   - Run `alembic upgrade head` to "manually" apply the migration

## Docs

- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
