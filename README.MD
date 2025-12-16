# 🚀 FastAPI Clean Architecture Boilerplate

A production-ready FastAPI backend using SQLAlchemy ORM, Alembic migrations, JWT authentication, and environment-based configuration.

## Python Version

- Python 3.7.9
- Pip 24.0

## Updates

- fastapi cli

## Available CLI Commands

### Make Commands

| Command                           | Description             |
| --------------------------------- | ----------------------- |
| `make:model <model_name>`         | Create a new model.     |
| `make:migration <migration_name>` | Create a new migration. |
| `make:module <module_name>`       | Create a new module.    |

### Database Commands

| Command      | Description             |
| ------------ | ----------------------- |
| `db:seed`    | Run database seeding.   |
| `db:migrate` | Run database migration. |

### Server Commands

| Command      | Description                 |
| ------------ | --------------------------- |
| `serve:dev`  | Serving development server. |
| `serve:prod` | Serving production server.  |

```

```

- swagger ui

## 📚 API Documentation (Swagger UI)

Visit: **http://127.0.0.1:5000/docs**

## for automatic Swagger API docs.

---

## 📦 Tech Stack

### **Core**

- **FastAPI** — High-performance API framework
- **Uvicorn** — ASGI server

### **Database & ORM**

- **SQLAlchemy** — ORM and database toolkit
- **Alembic** — Database migrations
- **PyMySQL** — MySQL database driver

### **Configuration & Validation**

- **Pydantic** — Data validation
- **pydantic-settings** — Typed settings management
- **python-dotenv** — `.env` loading
- **email-validator** — Email validation helper
- **python-multipart** — Form data handling

### **Security**

- **python-jose[cryptography]** — JWT tokens
- **passlib[bcrypt]** — Password hashing

---

## 📁 Project Structure

```
project/
│── app/
│ ├── main.py
│ ├── cli/
│ │ ├── commands/
│ │ ├── main.py
│ ├── core/
│ │ ├── config/
│ │ │ ├── app.py
│ │ ├── mailer/
│ │ ├── middleware/
│ │ ├── security.py
│ │ ├── jwt.py
│ ├── database/
│ │ ├── base.py
│ │ ├── session.py
│ │ ├── seeders/
│ ├── dependencies/
│ ├── models/
│ ├── schemas/
│ └── services/
│ └── repositories/
│ └── routes/
│ │ ├── api/
│ │ │ ├── auth/
│ │ │ ├── v1/
│ │ │ │ └── routes.py
│ │ ├── web.py
│ └── modules/
├─ tests/
│  ├─ test_login.py
│  └─ conftest.py
│── venv/
│── alembic.ini
│── requirements.txt
│── .env
│── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/rizalsk/Fast-API-Clean-Architecture-2025.git fastapiapp

cd fastapiapp
```

### 2. Create virtual environment

```
python -m venv venv source venv/bin/activate # Linux & Mac
venv\Scripts\activate # Windows
python -m venv venv source venv/Scripts/activate # Bash GIT
```

### 3. Install dependencies

`pip install -r requirements.txt`

---

## 🛠 Environment Variables (`.env`)

Example:

```
APP_NAME=FastAPI Clean Architecture
APP_URL=http://localhost
APP_PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=
DB_NAME=fastapidb

JWT_SECRET=supersecretkey123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=3
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 🗄 Database Setup

### Run Alembic migrations:

Run migrations using one of the following commands:

```bash
fastapi db:migrate
```

or

```bash
alembic upgrade head
```

### Create a new migration:

```
fastapi make:migration <migration_name>
```

or

```
alembic revision --autogenerate -m <migration_name>
```

---

### Seeder:

```
fastapi db:seed
```

or

```
python -m app.database.seeders.db_seeder
```

---

## ▶️ Running the Server

- Server Dev / Local

```
fastapi serve:dev
```

or

```
uvicorn app.main:app --reload` port: 8000
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

- Server Prod

```
fastapi serve:prod
```

---

## 🔐 Security

- Passwords hashed using **bcrypt**
- JWT authentication with **python-jose**
- Pydantic for safe request/response models

# Middleware

- Cors
- JWT
- Role and Permission
  `@router.get(
    "/", 
    response_model=List[UserResponse],
    dependencies=[Depends(has_access("Manage User:view"))], #middleware permission
)`

---

## 📬 Form & File Upload Support

`python-multipart` allows handling:

- multipart form data
- file uploads
- form fields with files

---

## 🧪 Testing

This project uses **pytest** and **httpx** for testing FastAPI. Make sure the virtual environment is active.

### Install dependencies

```bash
pip install pytest httpx pytest-asyncio pytest-benchmark
```

# Running a test

```
pytest tests/test_auth.py -v
```

# Running all tests

```
pytest -v
```

# Running Benchmark test

```
pytest tests/test_login_performance.py --benchmark-only
```

---

Copyright (c) 2025 RIZALSK

You are free to use, modify, distribute, and build upon this software for any purpose, commercial or non-commercial, with or without credit.
The software is provided “as is,” without any warranty.
