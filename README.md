# MoneyTracker Backend

Sync server for the MoneyTracker mobile app. The mobile is the source of truth — this server stores and returns a user's full financial dataset on demand.

## Stack

FastAPI · PostgreSQL · SQLAlchemy · JWT auth (python-jose) · bcrypt (passlib)

## Run

```bash
docker compose up --build
```

API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Endpoints

- `POST /auth/register` — create account, returns JWT
- `POST /auth/login` — returns JWT
- `POST /sync/push` — replace server dataset with mobile data *(requires Bearer token)*
- `GET /sync/pull` — fetch full dataset from server *(requires Bearer token)*

## Configuration

Set via environment variables or a `.env` file:

- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT signing secret (change before deploying)
- `TOKEN_EXPIRE_MINUTES` — token lifetime, default 10080 (one week)
