# Webtronics Test Task

## Description
Task description can be viewed [here](docs/TaskDescription.md).

## Deployment

### Docker
 - Copy example file
```shell
cp .env.example .env
```
 - Edit .env file, as in example:
```text
WT_DATABASE_URL=postgresql+asyncpg://prod:prod@database:5432/prod
WT_REDIS_URL=redis://cache/0
POSTGRES_USER=prod
POSTGRES_PASSWORD=prod
POSTGRES_DB=prod
WT_HUNTER_KEY=hunter_io_api_key
```
Redis URL can be left literally as in example.

If you want to change POSTGRES username, password or database -- change it in URL too.

If you do not want to user pre-signup [hunter.io](https://hunter.io/verify)  email verification -- just delete or comment out `WT_HUNTER_KEY` line


 - Run compose:
```shell
docker-compose up --build
```

### Bare metal

 - Install requirements:
```shell
poetry install --without dev,test
```
 - Install and configure [Postgresql](https://www.postgresql.org/) and [Redis](https://redis.io/).

 - Set environment variable `WT_DATABASE_URL` to postgresql url with dialect:
```shell
export WT_DATABASE_URL=postgresql+asyncpg://user:pass@127.0.0.1:5432/db
```
 - Set environmental variable `WT_REDIS_URL` to redis url:
```shell
export WT_REDIS_URL=redis://127.0.0.1:6379/0
```
 - (Optional) If you want to use pre-signup email check, set environmental variable `WT_HUNTER_KEY` to your personal [hunter.io](https://hunter.io/api-keys) API key:
```shell
export WT_HUNTER_KEY=myhunteriokey
```
 - Apply database migrations:
```shell
wt-db
```
 - Start app:
```shell
wt-api
```

## Testing
### Docker
 - Edit `src/webtronics/tests/.env` if needed

 - Run compose:
```shell
docker-compose -f src/webtronics/tests/docker-compose.yaml up --build --abort-on-container-exit
```

Test results will be shown in terminal:
![test_results_docker](docs/test_results_docker.png "test results docker")

When tests will be finished, containers will stop.

### Bare metal
 - Install requirements:
```shell
poetry install --without dev
```
 - Set environment variable WT_DATABASE_URL to testing postgresql url with dialect:
```shell
export WT_DATABASE_URL=postgresql+asyncpg://testuser:testpass@127.0.0.1:5432/testdb
```
 - Apply database migrations:
```shell
wt-db
```
 - Start app:
```shell
wt-test
```
Test results will be shown in terminal:
![test_results_baremetal](docs/test_results_baremetal.png "test results baremetal")