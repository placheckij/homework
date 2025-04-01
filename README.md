# TASK

## PREREQUISITES
- for running a containerized app: docker installed
- for running tests directly: poetry installed, virtual env activated (`$(poetry env activate)`)

## HOW TO START
- `docker compose up -d --build` will build an image with backend FastAPI app and pull postgresql image, then start both of them
- to run tests: `poetry run pytest tests`
- swagger (after running docker command mentioned above) will be available [here](http://localhost:3000/docs#) (if it's not, then please make sure you have port 3000 available, or update the ports mapping section in docker-compose.yml)

## CONTENTS DIRS
- alembic - contains alembic-specific files. Alembic is a library allowing to perform database structure migrations
- app - main sources directory
  - api - routing structure with endpoints
  - core - configuration stuff
  - db - database-related (async db client, ORM models)
  - models - domain objects definitions used mostly internally, also being a request / response structure on occassion
  - schemas - request / response structures
- tests - tests directory
- precommit - directory for custom scripts that are to be used by precommit
