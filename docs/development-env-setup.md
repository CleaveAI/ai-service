# Running the service locally

```bash
uv sync
source ./.venv/bin/activate
```

## Starting the Docker Containers

```bash
cd .docker/
docker compose up -d
```

## Running the server

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Running the Celery Workers

```bash
celery -A src.workers.main.celery_app worker --loglevel=info
```

### Triggering a task manually

```bash
celery -A src.workers.main.celery_app call workers.tasks.test.test_task
```

### Monitoring using flower

```bash
celery -A src.workers.main.celery_app flower --port=8300
```

## URLs

Once you run everything locally, you can access the following services:

| Service         | URL                     |
| --------------- | ----------------------- |
| Redis Insight   | <http://localhost:8100> |
| MongoDB Compass | <http://localhost:8200> |
| Celery Flower   | <http://localhost:8300> |
