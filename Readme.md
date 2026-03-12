# 🚀 TaskFlow API — Backend Engineering Journey

> A full-featured Team Task Management REST API built with FastAPI, PostgreSQL, Redis, Celery, WebSockets, Docker — covering every core backend engineering concept from scratch to production.

---

## 👨‍💻 About This Project

This project is a **structured learning journey** through backend engineering using Python + FastAPI.
Every session adds new files, new concepts, and new working code to the same real-world project.

**Goal:** Become a production-ready backend / AI-ML engineer by building one real system end to end.

---

## 🗂️ Project Structure

```
taskflow/
├── app/
│   ├── main.py                  # App entry point, lifespan, middleware
│   ├── config.py                # Pydantic settings, .env loading
│   ├── database.py              # Async SQLAlchemy engine + session
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── comment.py
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── token.py
│   ├── routers/                 # Route handlers split by domain
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── websocket.py
│   ├── services/                # Business logic layer
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   └── notification_service.py
│   ├── dependencies/            # FastAPI Depends() functions
│   │   ├── auth.py
│   │   └── database.py
│   ├── middleware/              # Custom middleware
│   │   ├── timing.py
│   │   └── request_id.py
│   └── utils/
│       ├── security.py          # JWT + password hashing
│       └── cache.py             # Redis helpers
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_projects.py
├── alembic/                     # DB migrations
├── .env                         # Environment variables (not committed)
├── .env.example                 # Template for env vars
├── requirements.txt             # All dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📚 Learning Curriculum — Session Log

| #   | Session              | Core Concept                                   | Files Created                                                                                      | Status  |
| --- | -------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------- |
| 01  | FastAPI Foundations  | ASGI vs WSGI, Uvicorn, App instance, Lifespan  | `main.py`, `config.py`, `.env`, `requirements.txt`                                                 | ✅ Done |
| 02  | Routes & Parameters  | Path params, Query params, HTTP methods        | `routers/__init__.py`, `routers/tasks.py`                                                          | ✅ Done |
| 03  | Pydantic Models      | BaseModel, Field, validators, nested models    | `schemas/enums.py`, `schemas/task.py`, `schemas/user.py`, `schemas/project.py`, `schemas/token.py` | ✅ Done |
| 04  | Request & Response   | response_model, HTTPException, status codes    | Update routers                                                                                     | ⏳ Next |
| 05  | Async / Await        | Event loop, async def, asyncio.gather          | All routes go async                                                                                | ⬜      |
| 06  | Database Setup       | Async SQLAlchemy, engine, session, Alembic     | `database.py`, `models/`                                                                           | ⬜      |
| 07  | Dependency Injection | Depends(), yield deps, chaining, DB session    | `dependencies/`                                                                                    | ⬜      |
| 08  | Authentication       | JWT, OAuth2, register, login, protected routes | `utils/security.py`, `routers/auth.py`                                                             | ⬜      |
| 09  | Routers & Structure  | APIRouter, prefix, tags, large app layout      | Refactor all routers                                                                               | ⬜      |
| 10  | Middleware           | Custom middleware, request ID, timing          | `middleware/`                                                                                      | ⬜      |
| 11  | Error Handling       | Global exception handlers, validation errors   | Update `main.py`                                                                                   | ⬜      |
| 12  | Background Tasks     | BackgroundTasks, Celery, Redis broker          | `services/notification_service.py`                                                                 | ⬜      |
| 13  | File Uploads         | UploadFile, multipart, storing files           | Update task router                                                                                 | ⬜      |
| 14  | Redis Caching        | Cache patterns, invalidation                   | `utils/cache.py`                                                                                   | ⬜      |
| 15  | Rate Limiting        | slowapi, per-IP limits                         | Update `main.py`                                                                                   | ⬜      |
| 16  | WebSockets           | Real-time updates, connection manager          | `routers/websocket.py`                                                                             | ⬜      |
| 17  | SSE / Streaming      | StreamingResponse, activity log                | Update routers                                                                                     | ⬜      |
| 18  | Testing              | pytest, AsyncClient, fixtures, overrides       | `tests/`                                                                                           | ⬜      |
| 19  | Docker + Deploy      | Dockerfile, docker-compose, Nginx, Gunicorn    | `Dockerfile`, `docker-compose.yml`                                                                 | ⬜      |

---

## 🛠️ Tech Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| Framework  | FastAPI 0.115                        |
| Server     | Uvicorn + Gunicorn                   |
| Database   | PostgreSQL 16 + AsyncPG              |
| ORM        | SQLAlchemy 2.0 (async)               |
| Migrations | Alembic                              |
| Cache      | Redis 7                              |
| Task Queue | Celery + Redis                       |
| Auth       | JWT (python-jose) + bcrypt (passlib) |
| Validation | Pydantic v2                          |
| Testing    | pytest + pytest-asyncio + httpx      |
| Containers | Docker + docker-compose              |

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/taskflow-api.git
cd taskflow-api

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your DB credentials

# 5. Run the server
uvicorn app.main:app --reload
```

Open: http://localhost:8000/docs

---

## 🗓️ Daily Streak Log

| Date       | Session    | What I Learned                                                                                            | Commits                                                  |
| ---------- | ---------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 2026-03-08 | Session 01 | FastAPI, ASGI vs WSGI, Uvicorn, lifespan, config                                                          | `init: project setup + main.py + config`                 |
| 2026-03-08 | Session 02 | Routes, path params, query params, HTTP methods, PUT vs PATCH, 204 status                                 | `feat: session 02 — routes, path params, query params`   |
| 2026-03-12 | Session 03 | Pydantic BaseModel, Field, Enums, field_validator, model_validator, schema separation (Create/Update/Out) | `feat: session 03 — pydantic schemas, enums, validators` |

## 🎯 Goals

- [ ] Complete all 19 sessions
- [ ] Full test coverage on auth + tasks
- [ ] Deploy to a cloud VM (Railway / Render / EC2)
- [ ] Write a blog post / LinkedIn post after completing

---

## 💡 Key Concepts Mastered

- **Session 01:** FastAPI is an ASGI framework. ASGI = async request handling. Uvicorn is the server that runs it. `lru_cache` on settings = read `.env` once and cache it.
- **Session 02:** Routes = HTTP method + URL path. Path params identify a resource (`/tasks/5`). Query params filter it (`?status=pending`). Specific routes must come before parameterized ones. PUT = full replace, PATCH = partial update, DELETE returns 204 (no body).
- **Session 03:** Pydantic validates raw JSON into typed Python objects automatically. Always have 3 schemas per model — Create (required fields), Update (all optional, for PATCH), Out (what you return, never expose password). `model_dump(exclude_unset=True)` on PATCH = only update what the client actually sent. `from_attributes=True` = read from SQLAlchemy ORM objects, not just dicts.

---

## 📎 Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0 Async Docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2 Docs](https://docs.pydantic.dev)
- [Alembic Docs](https://alembic.sqlalchemy.org)

---

_Built session by session. One concept at a time. No shortcuts._
