Berikut adalah penjelasan lengkap & profesional mengenai fungsi setiap direktori dalam arsitektur Clean Architecture FastAPI yang kita gunakan.
Struktur ini dirancang agar:

kode terorganisir,

mudah di-maintain,

scalable,

mudah di-testing,

mengikuti prinsip Separation of Concerns.

📁 Penjelasan Fungsi Setiap Direktori
1️⃣ core/

Berisi seluruh komponen “inti” aplikasi, seperti:

a. config.py

Memuat konfigurasi aplikasi dari .env menggunakan pydantic-settings.

Menyediakan akses mudah ke variabel lingkungan seperti DB URL, JWT_SECRET, dll.

b. security.py

Berisi fungsi hashing password (bcrypt).

Verifikasi password login.

Semua fitur security aplikasi.

c. jwt.py

Generate Access Token

Generate Refresh Token

Validasi token JWT
Ini dibuat terpisah agar mudah di-reuse di banyak bagian aplikasi.

Tujuan utama folder core/:
💡 Tempat fitur fundamental aplikasi yang tidak bergantung pada domain tertentu.

2️⃣ database/

Berisi semua konfigurasi database.

a. session.py

Membuat koneksi database (SQLAlchemy SessionLocal).

Menyediakan dependency untuk semua route.

b. base.py

Base class SQLAlchemy (declarative_base()).

Semua model mewarisi base ini.

c. migration/

Folder yang digunakan Alembic untuk migration.

Ini memuat:

env.py

versions/

Script upgrade/downgrade otomatis.

d. seeder.py

Untuk mengisi data awal (seperti admin user).

e. seeder/ (opsional)

Jika Anda ingin memiliki beberapa seed file (user_seed.py, article_seed.py, dll.)

Tujuan utama folder database/:
💡 Memisahkan konfigurasi dan resource database dari logic bisnis.

3️⃣ models/

Berisi ORM SQLAlchemy models, seperti:

user.py

article.py

banner_image.py

Models mencerminkan tabel database.

Tujuan utama folder models/:
💡 Representasi struktur database (Entity Layer).

4️⃣ schemas/

Berisi Pydantic Schema (DTO).
Ini digunakan untuk:

Validasi input dari client

Format output API

Menghindari return model SQLAlchemy secara raw (lebih aman)

Contoh:

ArticleCreate

ArticleResponse

BannerImageSchema

UserSchema

Tujuan utama folder schemas/:
💡 Memisahkan data “masuk & keluar API” dari data di database.

5️⃣ repositories/

Layer data access (DAO).
Semua operasi database dilakukan melalui repository, seperti:

UserRepository

ArticleRepository

BannerRepository

Contoh fungsi repository:

get_by_id()

create()

update()

delete()

Tujuan utama folder repositories/:
💡 Abstraksi operasi database sehingga service tidak berurusan langsung dengan SQLAlchemy.

6️⃣ services/

Layer bisnis aplikasi.
Berisi “Business Logic” seperti:

Validasi artikel sebelum insert

Upload file banner

Generate token saat login

Proses refresh token

Relasi antara Article dan Banner

Contoh:

AuthService

ArticleService

BannerService

Service menggunakan repository untuk CRUD.
Route hanya memanggil service → clean dan mudah di-testing.

Tujuan utama folder services/:
💡 Menampung seluruh business logic, terpisah dari DB dan route.

7️⃣ routes/

Folder API endpoint (Router Layer).
Semua route dipecah berdasarkan domain:

auth_route.py

article_route.py

banner_route.py

Route hanya bertugas:

menerima request

memanggil service

mengirim response

Route tidak berisi logic bisnis.

Tujuan utama folder routes/:
💡 Memisahkan endpoint API dari logic bisnis untuk meningkatkan keterbacaan dan modularitas.

8️⃣ assets/uploads/

Folder semua upload file, seperti:

Banner image

Image artikel

File lain yang diupload user

Tujuan utama folder assets/:
💡 Tempat penyimpanan file statis.

9️⃣ main.py

Entry point FastAPI:

Setup FastAPI

Register routers

Setup CORS

Load environment

Start app

🧩 Diagram Alur Clean Architecture
[ Client ]
↓
[ Routes ] --> menerima request → validasi dasar → panggil service
↓
[ Services ] --> berisi bisnis logic → memanggil repository
↓
[ Repositories ] → query SQLAlchemy
↓
[ Models ] (ORM) → database engine
↓
[ Database ] (MySQL)

🎯 Inti dari Clean Architecture ini:

1. Route = Interface

Hanya menerima input & mengembalikan output.

2. Service = Logic Bisnis

Semua aturan aplikasi.

3. Repository = Akses Database

SQLAlchemy CRUD.

4. Models = Struktur Database

Representasi tabel.

5. Schemas = Validasi Input/Output

Keamanan & konsistensi data API.

6. Core = fundamental sistem

Security, JWT, konfigurasi environment, utilitas penting.
