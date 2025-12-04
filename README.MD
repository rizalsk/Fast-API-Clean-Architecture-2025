# 🚀 FastAPI Clean Architecture

A production-ready FastAPI backend using SQLAlchemy ORM, Alembic migrations, JWT authentication, and environment-based configuration.

## Python Version

- Python 3.7.9

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
│ ├── core/
│ │ ├── config.py
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
│ │ │ ├── v1/
│ │ │ │ └── routes.py
│── venv/
│── alembic.ini
│── requirements.txt
│── .env
│── README.md
```

## ⚙️ Installation

### 1. Clone the repository

`git clone <your-repo-url> cd project`

### 2. Create virtual environment

`python -m venv venv source venv/bin/activate # Linux & Mac venv\Scripts\activate # Windows`
`python -m venv venv source venv/Scripts/activate # Bash GIT`

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

`alembic upgrade head`

### Create a new migration:

`alembic revision --autogenerate -m "description"`

---

### Seeder:

`python -m app.database.seeders.first_seeder`

---

## ▶️ Running the Server

`uvicorn app.main:app --reload` port: 8000
or
`uvicorn app.main:app --reload --host 0.0.0.0 --port 5000`

Visit: **http://127.0.0.1:5000/docs**

for automatic Swagger API docs.

---

## 🔐 Security

- Passwords hashed using **bcrypt**
- JWT authentication with **python-jose**
- Pydantic for safe request/response models

---

## 📬 Form & File Upload Support

`python-multipart` allows handling:

- multipart form data
- file uploads
- form fields with files

---

## 🧪 Testing (optional)

`pytest`

---

Copyright (c) 2025 RIZALSK

This software is licensed for personal use only. No part of this software may be
copied, modified, distributed, or used for any commercial or non-commercial
purpose by any person other than the copyright holder.

Anyone is free to use, modify, distribute, and build upon this software for any
purpose, with or without credit. The author provides no warranty of any kind.
