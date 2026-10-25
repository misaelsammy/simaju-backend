# SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu) - REST API

RESTful API backend untuk platform manajemen jadwal kegiatan, kolaborasi agenda grup/tim, pengulangan kegiatan rutin (*recurring events*), deteksi bentrok jadwal (*conflict detection*), serta pengingat otomatis (*reminders*). Proyek ini dibangun menggunakan **Node.js Express** dan **PostgreSQL (Neon Serverless)**, serta siap di-deploy secara serverless ke **Vercel**.

- **Teknologi**: Node.js, Express.js, PostgreSQL (Serverless via Neon / Supabase), Vercel  
- **Deployment URL**: `https://simaju-backend.vercel.app` *(sesuaikan dengan URL Vercel setelah di-deploy)*  

---

## 1. Deskripsi Singkat Project

**SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu)** adalah layanan backend REST API untuk memfasilitasi pengelolaan jadwal kegiatan, kolaborasi agenda grup/tim, pengulangan kegiatan rutin (*recurring events*), deteksi bentrok jadwal (*conflict detection*), serta pengingat otomatis (*reminders*).

API ini dibangun menggunakan arsitektur serverless Express.js yang siap di-deploy ke Vercel dan terhubung ke database relasional PostgreSQL di cloud (Neon.tech / Supabase).

---

## 2. Skema Database & ERD (Entity Relationship Diagram)

Database terdiri dari **7 tabel berelasi** dengan batasan Foreign Key dan integritas referensial (melampaui syarat minimal 5 tabel):

1. **`users`**: Menyimpan identitas pengguna (nama, email unik, hash password, instansi).
2. **`user_preferences`**: Relasi One-to-One dengan `users` untuk preferensi reminder default dan tema tampilan.
3. **`groups`**: Menyimpan grup kolaborasi jadwal yang dibuat oleh user.
4. **`group_members`**: Tabel pivot Many-to-Many antara `users` dan `groups`.
5. **`recurring_patterns`**: Menyimpan pola pengulangan jadwal (frekuensi: harian, mingguan, bulanan, dan tanggal berakhir).
6. **`events`** *(Resource Utama)*: Menyimpan seluruh jadwal kegiatan, terhubung ke `users`, `groups`, dan `recurring_patterns`.
7. **`reminders`**: Menyimpan daftar pengingat otomatis untuk event tertentu.

### Diagram ERD (Mermaid)

```mermaid
erDiagram
    users ||--|| user_preferences : "has preferences (1:1)"
    users ||--o{ groups : "creates"
    users ||--o{ group_members : "joins"
    groups ||--o{ group_members : "has members"
    users ||--o{ events : "owns"
    groups ||--o{ events : "contains shared"
    recurring_patterns ||--o{ events : "defines pattern for"
    events ||--o{ reminders : "triggers"

    users {
        serial user_id PK
        varchar name
        varchar email UK
        varchar password_hash
        varchar instansi
    }

    user_preferences {
        int user_id PK,FK
        int default_reminder_minutes
        varchar theme
    }

    groups {
        serial group_id PK
        varchar group_name
        int created_by FK
    }

    group_members {
        int group_id PK,FK
        int user_id PK,FK
        timestamp joined_at
    }

    recurring_patterns {
        serial pattern_id PK
        varchar frequency
        date end_date
    }

    events {
        serial event_id PK
        int user_id FK
        int group_id FK
        int pattern_id FK
        varchar title
        text description
        timestamp start_time
        timestamp end_time
        boolean is_skipped
    }

    reminders {
        serial reminder_id PK
        int event_id FK
        timestamp remind_at
        boolean is_sent
        varchar notification_type
    }
```

> **Catatan untuk dbdiagram.io / drawsql.app**:  
> Kode skema DBML tersedia pada file [`schema.dbml`](./schema.dbml). Anda bisa langsung copy-paste isinya ke [dbdiagram.io](https://dbdiagram.io) untuk mengunduh gambar diagram resolusi tinggi.

---

## 3. Daftar Endpoint REST API

### A. Health Check & Root

#### Root Status
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/`
- **Deskripsi**    : Memeriksa kesehatan server dan daftar tautan resource API
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "success": true,
    "message": "SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu) REST API is running successfully",
    "version": "1.0.0",
    "endpoints": {
      "users": "/api/users",
      "events": "/api/events",
      "groups": "/api/groups",
      "reminders": "/api/reminders"
    },
    "timestamp": "2026-10-25T12:00:00.000Z"
  }
  ```
- **Response Error (500)**:
  ```json
  {
    "error": "Terjadi kesalahan internal pada server"
  }
  ```

---

### B. Resource: Users & Preferences

#### 1. Registrasi Pengguna Baru
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/users/register`
- **Deskripsi**    : Mendaftarkan akun pengguna baru dan otomatis menginisialisasi record preferensi
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "name": "Alex Pratama",
    "email": "alex.pratama@simaju.app",
    "password": "RahasiaPassword123!",
    "instansi": "Divisi Teknologi Informasi",
    "default_reminder_minutes": 15,
    "theme": "dark"
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Registrasi pengguna berhasil",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama",
      "email": "alex.pratama@simaju.app",
      "instansi": "Divisi Teknologi Informasi"
    }
  }
  ```
- **Response Error (400)**:
  ```json
  {
    "error": "Field name, email, dan password wajib diisi"
  }
  ```

#### 2. Login Pengguna
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/users/login`
- **Deskripsi**    : Verifikasi kredensial pengguna untuk masuk ke sistem
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "email": "alex.pratama@simaju.app",
    "password": "RahasiaPassword123!"
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Login berhasil",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama",
      "email": "alex.pratama@simaju.app",
      "instansi": "Divisi Teknologi Informasi"
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Pengguna dengan email tersebut tidak ditemukan"
  }
  ```

#### 3. Mengambil Profil Pengguna
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/users/1`
- **Deskripsi**    : Mengambil data profil beserta preferensi jadwal
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil profil pengguna",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama",
      "email": "alex.pratama@simaju.app",
      "instansi": "Divisi Teknologi Informasi",
      "default_reminder_minutes": 15,
      "theme": "dark"
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Pengguna dengan ID 1 tidak ditemukan"
  }
  ```

#### 4. Memperbarui Profil Pengguna
- **Method**       : `PUT`
- **URL**          : `https://simaju-backend.vercel.app/api/users/1`
- **Deskripsi**    : Memperbarui nama, instansi, atau preferensi pengguna
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "name": "Alex Pratama, S.Kom.",
    "instansi": "Pusat Riset Data",
    "default_reminder_minutes": 30,
    "theme": "light"
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Profil pengguna berhasil diperbarui",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama, S.Kom.",
      "email": "alex.pratama@simaju.app",
      "instansi": "Pusat Riset Data",
      "default_reminder_minutes": 30,
      "theme": "light"
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Pengguna dengan ID 1 tidak ditemukan"
  }
  ```

---

### C. Resource Utama: Events (CRUD Lengkap)

#### 1. Mengambil Seluruh Jadwal (dengan Filter Rentang Tanggal & User)
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/events?user_id=1&start_date=2026-11-01&end_date=2026-11-30`
- **Deskripsi**    : Mengambil daftar kegiatan berdasarkan filter opsional
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar jadwal kegiatan",
    "total": 1,
    "data": [
      {
        "event_id": 1,
        "user_id": 1,
        "user_name": "Alex Pratama",
        "group_id": 1,
        "group_name": "Tim Pengembang SIMAJU",
        "pattern_id": null,
        "title": "Sprint Planning SIMAJU",
        "description": "Rapat mingguan pembahasan backlog dan arsitektur API",
        "start_time": "2026-11-01T09:00:00.000Z",
        "end_time": "2026-11-01T11:00:00.000Z",
        "is_skipped": false
      }
    ]
  }
  ```
- **Response Error (500)**:
  ```json
  {
    "error": "Terjadi kesalahan internal pada server"
  }
  ```

#### 2. Deteksi Bentrok Jadwal (Check Conflict)
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/events/check-conflict?user_id=1&start_time=2026-11-01T09:30:00&end_time=2026-11-01T10:30:00`
- **Deskripsi**    : Mengecek apakah terdapat jadwal yang tumpang-tindih untuk user tertentu
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "has_conflict": true,
    "total_conflicts": 1,
    "conflicts": [
      {
        "event_id": 1,
        "title": "Sprint Planning SIMAJU",
        "start_time": "2026-11-01T09:00:00.000Z",
        "end_time": "2026-11-01T11:00:00.000Z"
      }
    ]
  }
  ```
- **Response Error (400)**:
  ```json
  {
    "error": "Query parameter user_id, start_time, dan end_time wajib diisi"
  }
  ```

#### 3. Mengambil Detail Satu Jadwal
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/events/1`
- **Deskripsi**    : Mengambil detail jadwal beserta relasi reminder-nya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil detail jadwal",
    "data": {
      "event_id": 1,
      "user_id": 1,
      "user_name": "Alex Pratama",
      "user_email": "alex.pratama@simaju.app",
      "group_id": 1,
      "group_name": "Tim Pengembang SIMAJU",
      "pattern_id": null,
      "title": "Sprint Planning SIMAJU",
      "description": "Rapat mingguan pembahasan backlog dan arsitektur API",
      "start_time": "2026-11-01T09:00:00.000Z",
      "end_time": "2026-11-01T11:00:00.000Z",
      "is_skipped": false,
      "reminders": [
        {
          "reminder_id": 1,
          "remind_at": "2026-11-01T08:45:00.000Z",
          "is_sent": false,
          "notification_type": "email"
        }
      ]
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Jadwal dengan ID 1 tidak ditemukan"
  }
  ```

#### 4. Menambahkan Jadwal Baru (POST)
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/events`
- **Deskripsi**    : Menambah jadwal baru dengan validasi otomatis bentrok jadwal
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "user_id": 1,
    "group_id": 1,
    "title": "Presentasi Final Task Backend",
    "description": "Demo REST API dengan PostgreSQL dan Vercel",
    "start_time": "2026-11-10T10:00:00",
    "end_time": "2026-11-10T12:00:00",
    "allow_conflict": false
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Jadwal berhasil ditambahkan",
    "data": {
      "event_id": 4,
      "user_id": 1,
      "group_id": 1,
      "pattern_id": null,
      "title": "Presentasi Final Task Backend",
      "description": "Demo REST API dengan PostgreSQL dan Vercel",
      "start_time": "2026-11-10T10:00:00.000Z",
      "end_time": "2026-11-10T12:00:00.000Z",
      "is_skipped": false
    }
  }
  ```
- **Response Error (400)**:
  ```json
  {
    "error": "Jadwal bentrok dengan kegiatan yang sudah ada",
    "conflicts": [
      {
        "event_id": 1,
        "title": "Sprint Planning SIMAJU",
        "start_time": "2026-11-10T09:00:00.000Z",
        "end_time": "2026-11-10T11:00:00.000Z"
      }
    ]
  }
  ```

#### 5. Mengubah Data Jadwal (PUT)
- **Method**       : `PUT`
- **URL**          : `https://simaju-backend.vercel.app/api/events/1`
- **Deskripsi**    : Mengubah judul, deskripsi, waktu, atau grup jadwal
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "title": "Sprint Planning SIMAJU (Diperpanjang)",
    "description": "Pembahasan tambahan terkait skema ERD 7 tabel",
    "start_time": "2026-11-01T09:00:00",
    "end_time": "2026-11-01T11:30:00"
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Jadwal berhasil diperbarui",
    "data": {
      "event_id": 1,
      "user_id": 1,
      "group_id": 1,
      "pattern_id": null,
      "title": "Sprint Planning SIMAJU (Diperpanjang)",
      "description": "Pembahasan tambahan terkait skema ERD 7 tabel",
      "start_time": "2026-11-01T09:00:00.000Z",
      "end_time": "2026-11-01T11:30:00.000Z",
      "is_skipped": false
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Jadwal dengan ID 1 tidak ditemukan"
  }
  ```

#### 6. Menghapus Jadwal (DELETE)
- **Method**       : `DELETE`
- **URL**          : `https://simaju-backend.vercel.app/api/events/1`
- **Deskripsi**    : Menghapus kegiatan dari sistem kalender
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Jadwal 'Sprint Planning SIMAJU' berhasil dihapus",
    "deleted_id": 1
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Jadwal dengan ID 1 tidak ditemukan"
  }
  ```

---

### D. Resource: Groups & Kolaborasi

#### 1. Mengambil Daftar Seluruh Grup
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/groups`
- **Deskripsi**    : Menampilkan seluruh grup beserta jumlah anggotanya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar grup",
    "total": 2,
    "data": [
      {
        "group_id": 1,
        "group_name": "Tim Pengembang SIMAJU",
        "created_by": 1,
        "creator_name": "Alex Pratama",
        "total_members": 2
      }
    ]
  }
  ```

#### 2. Membuat Grup Baru
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/groups`
- **Deskripsi**    : Membuat grup baru dan otomatis memasukkan pembuat sebagai anggota pertama
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "group_name": "Divisi Cloud & DevOps",
    "created_by": 1
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Grup berhasil dibuat",
    "data": {
      "group_id": 3,
      "group_name": "Divisi Cloud & DevOps",
      "created_by": 1
    }
  }
  ```
- **Response Error (400)**:
  ```json
  {
    "error": "Field group_name dan created_by wajib diisi"
  }
  ```

#### 3. Menambahkan Anggota ke Grup (Pivot Many-to-Many)
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/groups/1/members`
- **Deskripsi**    : Mendaftarkan user ke dalam grup
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "user_id": 2
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Anggota berhasil ditambahkan ke dalam grup",
    "data": {
      "group_id": 1,
      "user_id": 2
    }
  }
  ```
- **Response Error (400)**:
  ```json
  {
    "error": "Pengguna sudah menjadi anggota grup ini"
  }
  ```

#### 4. Mengeluarkan Anggota dari Grup (DELETE)
- **Method**       : `DELETE`
- **URL**          : `https://simaju-backend.vercel.app/api/groups/1/members/2`
- **Deskripsi**    : Menghapus relasi anggota dari grup
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Anggota berhasil dikeluarkan dari grup",
    "removed": {
      "group_id": 1,
      "user_id": 2
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Anggota tidak ditemukan di grup tersebut"
  }
  ```

---

### E. Resource: Reminders (Pengingat)

#### 1. Mengambil Daftar Pengingat (Upcoming)
- **Method**       : `GET`
- **URL**          : `https://simaju-backend.vercel.app/api/reminders?upcoming=true`
- **Deskripsi**    : Mengambil pengingat yang belum terkirim dan akan jatuh tempo
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar pengingat",
    "total": 1,
    "data": [
      {
        "reminder_id": 1,
        "event_id": 1,
        "event_title": "Sprint Planning SIMAJU",
        "remind_at": "2026-11-01T08:45:00.000Z",
        "is_sent": false,
        "notification_type": "email",
        "user_name": "Alex Pratama",
        "user_email": "alex.pratama@simaju.app"
      }
    ]
  }
  ```

#### 2. Menambahkan Pengingat Baru (POST)
- **Method**       : `POST`
- **URL**          : `https://simaju-backend.vercel.app/api/reminders`
- **Deskripsi**    : Membuat pengingat untuk jadwal tertentu
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "event_id": 1,
    "remind_at": "2026-11-01T08:30:00",
    "notification_type": "push_notification"
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Pengingat berhasil dibuat",
    "data": {
      "reminder_id": 3,
      "event_id": 1,
      "remind_at": "2026-11-01T08:30:00.000Z",
      "is_sent": false,
      "notification_type": "push_notification"
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Jadwal dengan ID 1 tidak ditemukan"
  }
  ```

#### 3. Menandai Pengingat Terkirim (PATCH)
- **Method**       : `PATCH`
- **URL**          : `https://simaju-backend.vercel.app/api/reminders/1/sent`
- **Deskripsi**    : Mengubah status `is_sent` menjadi `true`
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Pengingat berhasil ditandai sebagai terkirim",
    "data": {
      "reminder_id": 1,
      "event_id": 1,
      "remind_at": "2026-11-01T08:45:00.000Z",
      "is_sent": true,
      "notification_type": "email"
    }
  }
  ```
- **Response Error (404)**:
  ```json
  {
    "error": "Pengingat dengan ID 1 tidak ditemukan"
  }
  ```

---

## 4. Cara Menjalankan Project Secara Lokal

### Prasyarat
- Node.js versi 18 atau lebih tinggi
- PostgreSQL (Lokal atau Cloud Neon.tech)

### Langkah Menjalankan:
1. **Buka folder proyek**:
   ```bash
   cd /home/ciel/Documents/simaju-backend
   ```
2. **Install dependensi**:
   ```bash
   npm install
   ```
3. **Konfigurasi Environment**:
   Salin `.env.example` ke `.env`:
   ```bash
   cp .env.example .env
   ```
   Isi nilai `DATABASE_URL` dengan connection string database PostgreSQL Anda (misalnya dari Neon.tech):
   ```env
   PORT=3000
   DATABASE_URL=postgresql://user:password@ep-sample.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ```
4. **Inisialisasi Tabel & Seeder Database**:
   ```bash
   npm run db:init
   npm run db:seed
   ```
5. **Jalankan Server Lokal**:
   ```bash
   npm run dev
   # Atau: npm start
   ```
   Akses `http://localhost:3000` di browser atau Postman.

---

## 5. Panduan Pengujian (Thunder Client / Postman)

1. Buka aplikasi **Postman** atau ekstensi **Thunder Client** di VS Code.
2. Klik tombol **Import** dan pilih file:
   [`simaju_api_collection.json`](./simaju_api_collection.json)
3. Sesuaikan variabel koleksi:
   - Untuk tes lokal: `base_url` = `http://localhost:3000`
   - Untuk tes deployment Vercel: `base_url` = `https://simaju-backend.vercel.app`
4. Jalankan setiap request pada koleksi untuk mengambil tangkapan layar (screenshot) sebagai bukti pengujian tugas.

---

## 6. Panduan Deployment ke Vercel

1. **Buat Repository di GitHub**:
   - Inisialisasi git di folder `simaju-backend`:
     ```bash
     cd /home/ciel/Documents/simaju-backend
     git init
     git add .
     git commit -m "feat: initial commit SIMAJU REST API"
     git branch -M main
     git remote add origin https://github.com/USERNAME/simaju-backend.git
     git push -u origin main
     ```
2. **Buat Database PostgreSQL di Neon.tech**:
   - Buka [neon.tech](https://neon.tech), buat project baru (Region: Singapore).
   - Salin connection string PostgreSQL.
3. **Deploy di Vercel**:
   - Buka [vercel.com](https://vercel.com) dan login dengan akun GitHub.
   - Klik **Add New Project**, pilih repository `simaju-backend`.
   - Di bagian **Environment Variables**, tambahkan:
     - Name: `DATABASE_URL`
     - Value: *(Connection string dari Neon.tech)*
   - Klik **Deploy**.
4. **Jalankan Inisialisasi Database**:
   - Dari terminal lokal (dengan file `.env` yang sudah diisi `DATABASE_URL` Neon):
     ```bash
     npm run db:init
     npm run db:seed
     ```
   - Selesai! Database cloud Anda kini sudah aktif dan Vercel API siap digunakan secara publik.
