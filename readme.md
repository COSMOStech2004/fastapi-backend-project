# FastAPI Backend Project

A production-style backend application built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT Authentication**, and **Role-Based Access Control**.

This project is created step by step to understand real-world backend development concepts such as API design, authentication, authorization, database migrations, logging, middleware, pagination, soft delete, audit logs, and clean project architecture.

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic Migrations
* Pydantic Validation
* JWT Authentication
* OAuth2 Password Bearer
* Passlib + bcrypt Password Hashing
* Python-dotenv
* Uvicorn
* Logging
* Middleware
* CORS

---

## Features

### Authentication

* User registration
* User login
* Password hashing
* JWT token generation
* Protected routes
* Current logged-in user
* Change password

### Authorization

* Role-Based Access Control
* Normal user role
* Admin role
* Admin-only routes
* Admin-only role update

### User Management

* Get profile
* Get users
* Get single user
* Full update using PUT
* Partial update using PATCH
* Duplicate email handling
* Response models to hide password

### Admin Features

* View all users
* Delete users
* Restore deleted users
* Permanently delete users
* Change user role
* View deleted users
* View audit logs

### Database Features

* PostgreSQL database
* SQLAlchemy ORM models
* Alembic database migrations
* Shared SQLAlchemy Base
* `created_at` and `updated_at` timestamps
* Soft delete using `is_deleted`
* Audit logs table

### API Improvements

* Pagination
* Search
* Filtering
* Sorting
* API versioning using `/api/v1`
* CORS middleware
* Request logging middleware
* Global exception handling

---

## Project Structure

```text
backend-learning/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│   ├── middleware.py
│   ├── exceptions.py
│   ├── security.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   └── admin_router.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── admin_service.py
│   │   └── audit_service.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── admin_schema.py
│   │   └── audit_schema.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_model.py
│   │   └── audit_log_model.py
│   │
│   └── dependencies/
│       ├── __init__.py
│       └── auth_dependency.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── logs/
│   └── app.log
│
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file in the root folder:

```env
DB_HOST=localhost
DB_NAME=fastapi_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_PORT=5432

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not upload `.env` to GitHub.

---

## Installation

### 1. Clone the project

```bash
git clone <your-repository-url>
cd backend-learning
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create a PostgreSQL database:

```text
fastapi_db
```

Update your `.env` file with correct PostgreSQL username and password.

---

## Alembic Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "migration message"
```

### Apply migrations

```bash
alembic upgrade head
```

### Check current migration

```bash
alembic current
```

---

## Run the Application

Run this command from the project root:

```bash
uvicorn app.main:app --reload
```

The server will start at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Auth Routes

| Method | Endpoint                       | Description             |
| ------ | ------------------------------ | ----------------------- |
| POST   | `/api/v1/auth/register`        | Register a new user     |
| POST   | `/api/v1/auth/login`           | Login and get JWT token |
| PATCH  | `/api/v1/auth/change-password` | Change password         |

---

### User Routes

| Method | Endpoint                  | Description                                            |
| ------ | ------------------------- | ------------------------------------------------------ |
| GET    | `/api/v1/users/profile`   | Get current logged-in user profile                     |
| GET    | `/api/v1/users/`          | Get users with pagination, search, filter, and sorting |
| GET    | `/api/v1/users/{user_id}` | Get single user                                        |
| PUT    | `/api/v1/users/{user_id}` | Full update user                                       |
| PATCH  | `/api/v1/users/{user_id}` | Partial update user                                    |

---

### Admin Routes

| Method | Endpoint                                  | Description             |
| ------ | ----------------------------------------- | ----------------------- |
| GET    | `/api/v1/admin/users`                     | Get all active users    |
| GET    | `/api/v1/admin/users/deleted`             | Get deleted users       |
| DELETE | `/api/v1/admin/users/{user_id}`           | Soft delete user        |
| PATCH  | `/api/v1/admin/users/{user_id}/restore`   | Restore deleted user    |
| DELETE | `/api/v1/admin/users/{user_id}/permanent` | Permanently delete user |
| PATCH  | `/api/v1/admin/users/{user_id}/role`      | Update user role        |
| GET    | `/api/v1/admin/audit-logs`                | View audit logs         |

---

## Authentication Flow

1. Register a user.
2. Login using email and password.
3. Backend verifies password.
4. Backend returns JWT access token.
5. Client sends token in future requests:

```text
Authorization: Bearer <access_token>
```

6. Protected routes verify token before allowing access.

---

## Authorization Flow

The project supports two roles:

```text
user
admin
```

Normal users can:

* view profile
* update user data
* change password

Admin users can:

* view all users
* delete users
* restore users
* permanently delete users
* update roles
* view audit logs

---

## Pagination, Search, Filter, and Sorting

User list APIs support:

```text
limit
offset
search
role
sort_by
sort_order
```

Example:

```text
/api/v1/users/?limit=10&offset=0&search=anshik&role=user&sort_by=created_at&sort_order=desc
```

Allowed sorting fields:

```text
id
name
email
age
role
created_at
updated_at
```

Allowed sorting orders:

```text
asc
desc
```

---

## Soft Delete System

Instead of permanently deleting users immediately, the project uses soft delete.

When admin deletes a user:

```text
is_deleted = true
deleted_at = current time
```

Soft-deleted users:

* disappear from normal user list
* cannot login
* cannot use old token
* can be restored by admin
* can be permanently deleted by admin

---

## Audit Logs

Important admin actions are stored in the `audit_logs` table.

Audit logs store:

```text
admin_id
target_user_id
action
details
created_at
```

Examples of audited actions:

```text
soft_delete
restore_user
permanent_delete
update_role
```

---

## Logging

Application logs are stored in:

```text
logs/app.log
```

Logs include:

* user registration
* login success/failure
* password changes
* admin actions
* validation errors
* unexpected server errors
* request method, path, status code, and process time

Do not log sensitive data such as:

```text
passwords
JWT tokens
secret keys
database passwords
```

---

## Middleware

The project includes middleware for:

* request logging
* response time tracking
* CORS support

Each response includes:

```text
X-Process-Time
```

---

## Security Practices Used

* Password hashing using bcrypt
* JWT token authentication
* Protected routes
* Role-based access control
* Response models to hide passwords
* Environment variables for secrets
* Duplicate email handling
* Global exception handling
* Admin-only dangerous actions
* Soft delete before permanent delete
* Audit logs for admin actions

---

## Common Commands

Run server:

```bash
uvicorn app.main:app --reload
```

Create migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migration:

```bash
alembic upgrade head
```

Install package:

```bash
pip install package_name
```

Update requirements:

```bash
pip freeze > requirements.txt
```

---

## Git Ignore

Recommended `.gitignore`:

```text
venv/
.env
__pycache__/
logs/
*.pyc
```

---

## Learning Concepts Covered

This project teaches:

* FastAPI basics
* REST APIs
* HTTP methods
* Pydantic validation
* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations
* JWT authentication
* OAuth2 password flow
* Dependency injection
* Middleware
* CORS
* Logging
* Global exception handling
* Role-based access control
* Pagination
* Search and filtering
* Sorting
* Soft delete
* Audit logs
* Clean backend architecture

---

## Future Improvements

Possible future features:

* Unit testing with Pytest
* Docker setup
* Docker Compose with PostgreSQL
* Refresh tokens
* Email verification
* Forgot password flow
* Rate limiting
* Background tasks
* File uploads
* Deployment to cloud
* CI/CD with GitHub Actions

---

## Author

Created as a step-by-step backend learning project using FastAPI and PostgreSQL.
