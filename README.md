# Inventory & Order Management System

A full-stack, containerized application for managing products, customers, orders, and
inventory. Orders are multi-line, stock is tracked and decremented atomically, and a
dashboard summarizes the business at a glance.

## Tech stack

- **Backend:** Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic (migrations), PostgreSQL
- **Frontend:** React (JavaScript) + Vite, React Router, Axios, Tailwind CSS
- **Containerization:** Docker + Docker Compose
- **Tooling:** ruff (lint + format), mypy (strict), pytest (via testcontainers)

## Features

- **Products** — full CRUD; unique SKU; non-negative price and quantity.
- **Customers** — create, list, delete; unique email.
- **Orders** — multi-line orders; stock validated and decremented in a single transaction
  (insufficient stock is rejected with no side effects); total computed by the backend.
- **Dashboard** — totals for products, customers, orders, plus low-stock products.
- **Pagination** — all list endpoints are paginated (`limit`/`offset`, envelope response).

## Architecture

Three services, orchestrated by Docker Compose:

```
frontend (nginx)  ──/api──▶  backend (FastAPI)  ──▶  db (PostgreSQL)
```

The frontend calls the relative path `/api`; in the container nginx proxies `/api` to the
backend, and in local dev the Vite dev server proxies it. The browser never needs the
backend host. The backend is layered `routers → services → repositories → models`.

## Prerequisites

- Docker and Docker Compose
- For local (non-Docker) development: Node 20+ and Python 3.12+

## Setup

```bash
cp .env.example .env      # then edit credentials as needed
```

Environment variables (see `.env.example`):

| Variable              | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `POSTGRES_USER`       | Postgres user                                        |
| `POSTGRES_PASSWORD`   | Postgres password                                    |
| `POSTGRES_DB`         | Postgres database name                               |
| `POSTGRES_HOST`       | DB host (compose service name `db`)                  |
| `POSTGRES_PORT`       | DB port (default 5432)                               |
| `LOW_STOCK_THRESHOLD` | Products below this quantity are flagged low-stock   |

The backend composes its connection string from these parts; no full URL is hardcoded.

## Run with Docker (recommended)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

The backend applies database migrations (`alembic upgrade head`) automatically on startup.
Postgres data persists in a named volume (`pgdata`).

## Local development (without Docker)

Backend (needs a running Postgres; set the `POSTGRES_*` vars in the environment or a
`backend/.env`):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend (the Vite dev server proxies `/api` to http://localhost:8000):

```bash
cd frontend
npm install
npm run dev
```

## Tests and quality

```bash
cd backend
pytest                 # spins up a throwaway Postgres via testcontainers (Docker required)
ruff check .           # lint
mypy app               # strict type checking
```

## Database migrations

Migrations are managed by Alembic (one migration per entity) and applied automatically when
the backend container starts. To create a new migration after changing a model:

```bash
cd backend
alembic revision --autogenerate -m "your message"
alembic upgrade head
```

## API overview

All endpoints are under the API root (`/api` via the proxy, or directly on the backend).
List endpoints accept `?limit=` (1–100, default 50) and `?offset=` and return a paginated
envelope: `{ "items": [...], "total": N, "limit": L, "offset": O }`.

| Method | Path              | Description                                  |
| ------ | ----------------- | -------------------------------------------- |
| GET    | `/products`       | List products (paginated)                    |
| POST   | `/products`       | Create a product                             |
| GET    | `/products/{id}`  | Get a product                                |
| PUT    | `/products/{id}`  | Update a product                             |
| DELETE | `/products/{id}`  | Delete a product                             |
| GET    | `/customers`      | List customers (paginated)                   |
| POST   | `/customers`      | Create a customer                            |
| GET    | `/customers/{id}` | Get a customer                               |
| DELETE | `/customers/{id}` | Delete a customer                            |
| GET    | `/orders`         | List orders, summary shape (paginated)       |
| POST   | `/orders`         | Create an order                              |
| GET    | `/orders/{id}`    | Get an order with line items                 |
| DELETE | `/orders/{id}`    | Delete an order                              |
| GET    | `/dashboard`      | Totals + low-stock products                  |

Create an order with:

```json
{ "customer_id": 1, "items": [{ "product_id": 1, "quantity": 2 }] }
```

Order detail returns nested objects (the order-time `unit_price` is kept per line, since a
product's price may change later):

```json
{
  "id": 1, "total_amount": "69.97", "created_at": "...",
  "customer": { "id": 1, "full_name": "Ada Lovelace" },
  "items": [
    { "id": 1, "quantity": 2, "unit_price": "9.99",
      "product": { "id": 1, "name": "Widget", "sku": "W1" } }
  ]
}
```

## Project structure

```
.
├── docker-compose.yml          # db + backend + frontend
├── .env.example
├── backend/
│   ├── Dockerfile, entrypoint.sh
│   ├── alembic/                # migrations
│   └── app/
│       ├── core/               # config, database
│       ├── models/             # SQLAlchemy ORM
│       ├── schemas/            # Pydantic models
│       ├── repositories/       # DB access
│       ├── services/           # business logic
│       └── routers/            # FastAPI endpoints
└── frontend/
    ├── Dockerfile, nginx.conf
    └── src/
        ├── api/                # axios client + per-entity modules
        ├── hooks/              # data-fetching hooks
        ├── components/         # layout + shared UI
        └── pages/              # Dashboard, Products, Customers, Orders
```

## Deployment

The Docker/nginx frontend container is used for local Docker Compose. For cloud hosting,
the frontend deploys as a static build to Vercel or Netlify and the backend to Render or
Railway; the frontend reaches the backend either via a platform rewrite of `/api` to the
backend URL or by setting `VITE_API_BASE_URL` at build time.
