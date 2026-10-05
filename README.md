# FastAPI Blog API

A small REST API for managing users and blog posts, built with **FastAPI**, **SQLAlchemy** and **MySQL**. It supports user registration, password hashing (bcrypt) and JWT-based login.

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Using the API](#using-the-api)
- [Endpoint reference](#endpoint-reference)
- [Data models](#data-models)

## Features

- Create and list users, fetch a user by ID
- Full CRUD for blog posts
- Passwords stored as bcrypt hashes
- Login with email + password, returns a JWT bearer token
- Interactive API docs generated automatically (Swagger UI and ReDoc)
- Database tables are created automatically on startup

## Tech stack

| Purpose            | Library                |
| ------------------ | ---------------------- |
| Web framework      | FastAPI + Uvicorn      |
| ORM                | SQLAlchemy 2.x         |
| Database driver    | PyMySQL (MySQL)        |
| Validation         | Pydantic 2             |
| Password hashing   | passlib + bcrypt       |
| Tokens             | PyJWT                  |

## Project structure

```
.
├── main.py              # App entry point; registers routers, creates tables
├── database.py          # DB engine, session factory, get_db dependency
├── models.py            # SQLAlchemy models (User, Blog)
├── routers/
│   ├── authentication.py  # POST /login
│   ├── user.py            # /user, /users, /user/{id}
│   └── blog.py            # /blog, /blog/{id}
├── schemas/             # Pydantic request/response schemas
│   ├── blog.py
│   ├── user.py
│   ├── login.py
│   └── token.py
├── libs/
│   ├── hashing.py       # bcrypt hash / verify helpers
│   ├── token.py         # JWT creation and verification
│   └── oAuth2.py        # get_current_user dependency (bearer token)
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.10+
- A running MySQL server

### 1. Install dependencies

```powershell
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

> If `pip` complains about the encoding of `requirements.txt`, re-save the file as UTF-8 (it is currently UTF-16).

### 2. Create the database

```sql
CREATE DATABASE fast_api;
```

The `users` and `blogs` tables are created automatically the first time the app starts.

### 3. Run the server

```powershell
uvicorn main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.

| URL                                | What it is                    |
| ---------------------------------- | ----------------------------- |
| <http://127.0.0.1:8000/docs>       | Swagger UI (try requests here) |
| <http://127.0.0.1:8000/redoc>      | ReDoc reference               |
| <http://127.0.0.1:8000/openapi.json> | Raw OpenAPI schema          |

## Configuration

Settings are currently **hard-coded** in two files. Edit them to match your environment:

| Setting                       | File                              | Default                  |
| ----------------------------- | --------------------------------- | ------------------------ |
| DB user / password / host / port / name | [database.py](database.py) | `root` / *(empty)* / `localhost` / `3306` / `fast_api` |
| JWT `SECRET_KEY`              | [libs/token.py](libs/token.py)    | a sample key             |
| JWT `ALGORITHM`               | [libs/token.py](libs/token.py)    | `HS256`                  |
| Token lifetime                | [libs/token.py](libs/token.py)    | 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`; see [limitations](#known-limitations)) |

**Before deploying anywhere real, replace `SECRET_KEY` with your own secret** (e.g. `openssl rand -hex 32`) and keep it out of version control.

## Using the API

A typical flow, using `curl`:

**1. Register a user**

```bash
curl -X POST http://127.0.0.1:8000/user \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "secret123"}'
```

**2. Log in to get a token**

Login uses the OAuth2 *password form* format (form fields, not JSON). The `username` field is the user's **email**.

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=alice@example.com&password=secret123"
```

```json
{ "access_token": "eyJhbGciOi...", "token_type": "bearer" }
```

**3. Call a protected endpoint**

```bash
curl http://127.0.0.1:8000/blog \
  -H "Authorization: Bearer <access_token>"
```

**4. Create a blog post**

```bash
curl -X POST http://127.0.0.1:8000/blog \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "description": "My first post", "published": true}'
```

> Tip: in Swagger UI (`/docs`) click **Authorize**, enter your email as *username* and your password, and the token is attached to requests for you.

## Endpoint reference

### Authentication

| Method | Path     | Auth | Description                         |
| ------ | -------- | ---- | ----------------------------------- |
| POST   | `/login` | No   | Exchange email + password for a JWT |

- **Body** (form-encoded): `username` (email), `password`
- **200**: `{ "access_token": "...", "token_type": "bearer" }`
- **404**: `Invalid credentials`

### Users

| Method | Path          | Auth | Description        | Success |
| ------ | ------------- | ---- | ------------------ | ------- |
| POST   | `/user`       | No   | Create a user      | 201     |
| GET    | `/users`      | No   | List all users     | 200     |
| GET    | `/user/{id}`  | No   | Get a user by ID   | 200     |

- `POST /user` body: `{ "name": str, "email": str, "password": str }`
- `GET /users` and `GET /user/{id}` return **404** `No User Found` when nothing matches.
- Emails must be unique.

### Blogs

| Method | Path          | Auth         | Description          | Success |
| ------ | ------------- | ------------ | -------------------- | ------- |
| GET    | `/blog`       | **Bearer**   | List all blog posts  | 200     |
| GET    | `/blog/{id}`  | No           | Get a post by ID     | 200     |
| POST   | `/blog`       | No           | Create a post        | 201     |
| PUT    | `/blog/{id}`  | No           | Update a post        | 202     |
| DELETE | `/blog/{id}`  | No           | Delete a post        | 204     |

- `POST` / `PUT` body: `{ "title": str, "description": str, "published": bool (default true) }`
- `GET /blog` returns **404** `Blog not found` when there are no posts; `GET /blog/{id}` and `PUT /blog/{id}` return the same for an unknown ID.
- Successful responses are wrapped: `{ "data": ... }`.
             |

## Data models

**User** (`users`)

| Column     | Type         | Notes                 |
| ---------- | ------------ | --------------------- |
| `id`       | Integer (PK) |                       |
| `name`     | String(100)  |                       |
| `email`    | String(100)  | unique                |
| `password` | String(100)  | bcrypt hash           |

**Blog** (`blogs`)

| Column        | Type         | Notes                          |
| ------------- | ------------ | ------------------------------ |
| `id`          | Integer (PK) |                                |
| `title`       | String(100)  | required, unique               |
| `description` | String(500)  | required                       |
| `published`   | Integer      | default `0`                    |
| `user_id`     | Integer (FK) | references `users.id`          |

A user has many blogs; each blog has one creator.

