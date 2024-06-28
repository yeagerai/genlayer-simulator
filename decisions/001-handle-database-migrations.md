# Handle database migrations with SQLAlchemy + Alembic

- Status: proposed
- Deciders: Agustín Díaz
- Date: 2024-06-26

## Context and Problem Statement

Given the continuous evolution of the code and the database model, we need to decide how to handle database migrations.

How can we handle database migrations?

## Decision Drivers

- As a developer, I want to be able to move between branches with automatic database schema migrations.
- As a user, I want to be able to use newer application releases without losing data.

## Considered Options

- Database migration tools
- Database schema versioning

## Decision Outcome

Chosen option: [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/en/latest/), because it's the best of both approaches:

- SQLAlchemy allows us to define an almost declarative database schema in Python code
- SQLAlchemy as an ORM will simplify the interaction with the database, and reduce errors on manual SQL queries and mappings
- Alembic allows us to generate migration files in Python from the differences between the current schema and the desired schema
- Alembic it's integrated with SQLAlchemy
- Alembic allows us to downgrade migrations if needed
- Wide community adoption, support, and documentation
- Great integration with PostgreSQL, the database we are using

### [Example](https://www.youtube.com/watch?v=i9RX03zFDHU)

### Consequences

- We'll add SQLAlchemy and Alembic as dependencies
- We'll integrate it with our codebase
  1. Define database models with SQLAlchemy
  1. Configure Alembic
  1. Generate the initial migration
  1. Run the migration as part of the deployment process: a new service in the docker-compose file

## Pros and Cons of the Options

### Database migration tools

Examples include [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment), [Django migrations](https://docs.djangoproject.com/en/5.0/topics/migrations/).

- Good, because it allows us to run Python code, handy for complex migrations
- Good, because usually integrates well with ORMs (sqlalchemy + alembic)
- Good, because usually allow both incremental changes and full schema generation like mentioned in https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch
- Bad, because it requires manual intervention to create migration files
- Bad, because git merge conflicts can arise when multiple developers create migration files

### Database schema versioning

Examples include Prisma, Drizzle, [Atlas](https://github.com/ariga/atlas).

- Good, because we can have declarative schema definitions
- Good, because many operations are automatically handled
- Bad, because it's not as flexible as writing Python code
- Bad, because it's a new tool that most developers are not familiar with
