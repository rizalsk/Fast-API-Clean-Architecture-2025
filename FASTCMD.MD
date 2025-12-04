1. create dir clean architectur
2. create virtual env

Microsoft Visual C++ 14.0 or greater is required.

```
python -m venv venv
# source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
source venv/Scripts/activate #bash

pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings \
    pymysql python-jose[cryptography] passlib[bcrypt] python-dotenv \
    email-validator python-multipart

```

env.py database

```
from app.database.session import Base
target_metadata = Base.metadata
```

```
alembic init app/database/migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

SEEDER

```
python -m app.database.seeder
```

RUN

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
// OR
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

TEST

```
13. Test Requests (curl / httpie)

Register

http POST http://localhost:8000/auth/register username="test" email="test@mail.com" password="secret"


Login

http POST http://localhost:8000/auth/login username="test" password="secret"


Create Article

http POST http://localhost:8000/articles/ title="Title" content="Content" banner_image_id:=1 "Authorization:Bearer <ACCESS_TOKEN>"


List Articles

http GET http://localhost:8000/articles/ "Authorization:Bearer <ACCESS_TOKEN>"
```

Clear cache:

```
find . -name "__pycache__" -type d -exec rm -rf {} +
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
 OR
# bash
Get-ChildItem -Recurse -Directory -Force -Filter "__pycache__" | Remove-Item -Recurse -Force
```
