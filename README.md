# SIMAJU REST API

> **Sistem Informasi Manajemen Jadwal Terpadu** — Layanan backend RESTful API untuk manajemen kalender kegiatan, agenda kolaboratif tim, perulangan acara berkala (*recurring events*), deteksi bentrok jadwal (*conflict detection*), dan pengingat otomatis (*reminders*).

Dibangun menggunakan arsitektur modern **Node.js**, **Express.js**, dan **PostgreSQL (Neon Serverless)**, serta siap di-deploy secara serverless ke **Vercel**.

- **Deployment URL**: [`https://simaju-backend.vercel.app`](https://simaju-backend.vercel.app)
- **Database**: PostgreSQL (Serverless via Neon / Supabase)
- **Runtime**: Node.js v18+

---

## Fitur Utama

- 📅 **Manajemen Jadwal Lengkap**: Operasi CRUD (Create, Read, Update, Delete) agenda kegiatan dengan validasi rentang waktu.
- ⚡ **Deteksi Bentrok Jadwal (Conflict Detection)**: Algoritma validasi otomatis untuk mencegah agenda tumpang tindih pada waktu yang sama.
- 🔁 **Perulangan Jadwal (Recurring Events)**: Konfigurasi pola perulangan (harian, mingguan, bulanan) dengan batas tanggal akhir.
- 👥 **Kolaborasi Agenda Grup**: Pembuatan ruang kerja tim, manajemen anggota (pivot many-to-many), dan pembagian agenda bersama.
- ⏰ **Sistem Pengingat (Reminders)**: Penjadwalan pengingat otomatis sebelum kegiatan dimulai beserta penanda status terkirim.

---

## Diagram Relasi Basis Data (ERD)

Basis data dirancang menggunakan relasi referensial antartabel PostgreSQL dengan integritas data dan batasan *Foreign Key*:

```mermaid
erDiagram
    USERS ||--|| USER_PREFERENCES : "has"
    USERS ||--o{ GROUPS : "creates"
    USERS ||--o{ GROUP_MEMBERS : "joins"
    GROUPS ||--o{ GROUP_MEMBERS : "has"
    USERS ||--o{ EVENTS : "owns"
    GROUPS ||--o{ EVENTS : "shares"
    RECURRING_PATTERNS ||--o{ EVENTS : "defines"
    EVENTS ||--o{ REMINDERS : "triggers"

    USERS {
        int user_id PK
        string name
        string email UK
        string password_hash
        string instansi
    }

    USER_PREFERENCES {
        int user_id PK
        int default_reminder_minutes
        string theme
    }

    GROUPS {
        int group_id PK
        string group_name
        int created_by FK
    }

    GROUP_MEMBERS {
        int group_id PK,FK
        int user_id PK,FK
        timestamp joined_at
    }

    RECURRING_PATTERNS {
        int pattern_id PK
        string frequency
        date end_date
    }

    EVENTS {
        int event_id PK
        int user_id FK
        int group_id FK
        int pattern_id FK
        string title
        text description
        timestamp start_time
        timestamp end_time
        boolean is_skipped
    }

    REMINDERS {
        int reminder_id PK
        int event_id FK
        timestamp remind_at
        boolean is_sent
        string notification_type
    }
```

### Penjelasan Entitas & Relasi Tabel

1. **`users`**: Menyimpan identitas akun pengguna dan instansi.
2. **`user_preferences`**: Relasi One-to-One dengan `users` untuk preferensi tema dan default waktu pengingat.
3. **`groups`**: Menyimpan grup kerja/tim kolaborasi yang dibuat oleh pengguna.
4. **`group_members`**: Tabel perantara (pivot Many-to-Many) antara pengguna dan grup.
5. **`recurring_patterns`**: Definisi pola frekuensi perulangan agenda dan tanggal berakhir.
6. **`events`**: Entitas utama penyimpanan seluruh jadwal kegiatan personal maupun grup.
7. **`reminders`**: Menyimpan data pengingat otomatis untuk setiap kegiatan.

---

## Dokumentasi Endpoint API

Base URL: `https://simaju-backend.vercel.app` (atau `http://localhost:3000` untuk lingkungan lokal).

### A. Health Check

#### Status Layanan
- **Method**       : `GET`
- **URL**          : `/`
- **Deskripsi**    : Memeriksa kesiapan server dan daftar endpoint aktif
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

---

### B. Pengguna & Autentikasi (`/api/users`)

#### 1. Mengambil Seluruh Pengguna
- **Method**       : `GET`
- **URL**          : `/api/users`
- **Deskripsi**    : Mengambil seluruh daftar pengguna beserta preferensi tampilannya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar pengguna",
    "total": 6,
    "data": [
      {
        "user_id": 1,
        "name": "Alex Pratama, S.Kom.",
        "email": "alex@simaju.app",
        "instansi": "Pusat Riset Data",
        "default_reminder_minutes": 30,
        "theme": "system"
      }
    ]
  }
  ```

#### 2. Registrasi Pengguna
- **Method**       : `POST`
- **URL**          : `/api/users/register`
- **Deskripsi**    : Mendaftarkan akun pengguna baru sekaligus menginisialisasi record preferensi bawaan
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "name": "Citra Dewi",
    "email": "citra.dewi@simaju.app",
    "password": "Password123!",
    "instansi": "Biro Perencanaan dan Keuangan",
    "default_reminder_minutes": 15,
    "theme": "light"
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Registrasi pengguna berhasil",
    "data": {
      "user_id": 7,
      "name": "Citra Dewi",
      "email": "citra.dewi@simaju.app",
      "instansi": "Biro Perencanaan dan Keuangan"
    }
  }
  ```

#### 3. Login Pengguna
- **Method**       : `POST`
- **URL**          : `/api/users/login`
- **Deskripsi**    : Memverifikasi email dan password untuk autentikasi pengguna
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "email": "alex@simaju.app",
    "password": "hashed_pass_alex"
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Login berhasil",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama, S.Kom.",
      "email": "alex@simaju.app",
      "instansi": "Pusat Riset Data"
    }
  }
  ```

#### 4. Mengambil Profil Pengguna
- **Method**       : `GET`
- **URL**          : `/api/users/:id`
- **Deskripsi**    : Mengambil detail informasi akun pengguna dan preferensi bawaannya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil profil pengguna",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama, S.Kom.",
      "email": "alex@simaju.app",
      "instansi": "Pusat Riset Data",
      "default_reminder_minutes": 30,
      "theme": "system"
    }
  }
  ```

#### 5. Memperbarui Profil Pengguna
- **Method**       : `PUT`
- **URL**          : `/api/users/:id`
- **Deskripsi**    : Memperbarui nama, instansi, atau pengaturan tema dan pengingat pengguna
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "name": "Alex Pratama, M.Kom.",
    "instansi": "Pusat Riset Data Nasional",
    "default_reminder_minutes": 45,
    "theme": "dark"
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Profil dan preferensi pengguna berhasil diperbarui",
    "data": {
      "user_id": 1,
      "name": "Alex Pratama, M.Kom.",
      "email": "alex@simaju.app",
      "instansi": "Pusat Riset Data Nasional",
      "default_reminder_minutes": 45,
      "theme": "dark"
    }
  }
  ```

---

### C. Manajemen Jadwal (`/api/events`)

#### 1. Mengambil Daftar Seluruh Jadwal
- **Method**       : `GET`
- **URL**          : `/api/events` (opsional filter query: `?user_id=1&start_date=2026-11-01&end_date=2026-11-30`)
- **Deskripsi**    : Mengambil daftar kegiatan kalender dengan filter rentang tanggal dan user
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar jadwal kegiatan",
    "total": 8,
    "data": [
      {
        "event_id": 2,
        "user_id": 1,
        "user_name": "Alex Pratama, S.Kom.",
        "group_id": null,
        "group_name": null,
        "pattern_id": 1,
        "recurring_frequency": "weekly",
        "title": "Evaluasi Proyek Mingguan",
        "description": "Review sprint progres Q4 di Ruang Rapat Utama A",
        "start_time": "2026-11-03T14:00:00.000Z",
        "end_time": "2026-11-03T16:00:00.000Z",
        "is_skipped": false
      }
    ]
  }
  ```

#### 2. Deteksi Bentrok Jadwal (Check Conflict)
- **Method**       : `GET`
- **URL**          : `/api/events/check-conflict?user_id=1&start_time=2026-11-10T09:00:00&end_time=2026-11-10T11:00:00`
- **Deskripsi**    : Memeriksa apakah calon agenda bertabrakan dengan agenda lain yang sudah terdaftar
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Pengecekan konflik selesai",
    "data": {
      "has_conflict": true,
      "conflict_count": 1,
      "conflicts": [
        {
          "event_id": 4,
          "title": "Presentasi Final Task Backend",
          "start_time": "2026-11-10T10:00:00.000Z",
          "end_time": "2026-11-10T12:00:00.000Z"
        }
      ]
    }
  }
  ```

#### 3. Mengambil Detail Jadwal
- **Method**       : `GET`
- **URL**          : `/api/events/:id`
- **Deskripsi**    : Mengambil detail satu kegiatan beserta daftar pengingat yang terhubung
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil detail jadwal",
    "data": {
      "event_id": 2,
      "user_id": 1,
      "user_name": "Alex Pratama, S.Kom.",
      "user_email": "alex@simaju.app",
      "group_id": null,
      "group_name": null,
      "pattern_id": 1,
      "recurring_frequency": "weekly",
      "recurring_end_date": "2026-12-31",
      "title": "Evaluasi Proyek Mingguan",
      "description": "Review sprint progres Q4 di Ruang Rapat Utama A",
      "start_time": "2026-11-03T14:00:00.000Z",
      "end_time": "2026-11-03T16:00:00.000Z",
      "is_skipped": false,
      "reminders": [
        {
          "reminder_id": 3,
          "remind_at": "2026-11-03T13:45:00.000Z",
          "notification_type": "email",
          "is_sent": false
        }
      ]
    }
  }
  ```

#### 4. Menambahkan Jadwal Baru (POST)
- **Method**       : `POST`
- **URL**          : `/api/events`
- **Deskripsi**    : Menambahkan agenda mandiri baru ke kalender sistem (dengan validasi bentrok jadwal)
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "user_id": 1,
    "title": "Sosialisasi Roadmap AI Nasional",
    "description": "Pembahasan implementasi roadmap kecerdasan buatan terpadu",
    "start_time": "2026-12-05T09:00:00",
    "end_time": "2026-12-05T11:30:00",
    "allow_conflict": true
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Jadwal berhasil ditambahkan",
    "data": {
      "event_id": 9,
      "user_id": 1,
      "group_id": null,
      "pattern_id": null,
      "title": "Sosialisasi Roadmap AI Nasional",
      "description": "Pembahasan implementasi roadmap kecerdasan buatan terpadu",
      "start_time": "2026-12-05T09:00:00.000Z",
      "end_time": "2026-12-05T11:30:00.000Z",
      "is_skipped": false
    }
  }
  ```

#### 5. Menambahkan Jadwal Berulang (Recurring Event)
- **Method**       : `POST`
- **URL**          : `/api/events`
- **Deskripsi**    : Menambahkan agenda dengan frekuensi perulangan (`daily`, `weekly`, `monthly`)
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "user_id": 1,
    "title": "Rapat Koordinasi Rutin Divisi IT",
    "description": "Sinkronisasi sprint mingguan",
    "start_time": "2026-12-01T13:00:00",
    "end_time": "2026-12-01T14:30:00",
    "frequency": "weekly",
    "end_date": "2026-12-31",
    "allow_conflict": true
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Jadwal berhasil ditambahkan",
    "data": {
      "event_id": 10,
      "user_id": 1,
      "group_id": null,
      "pattern_id": 2,
      "title": "Rapat Koordinasi Rutin Divisi IT",
      "start_time": "2026-12-01T13:00:00.000Z",
      "end_time": "2026-12-01T14:30:00.000Z",
      "is_skipped": false
    }
  }
  ```

#### 6. Mengubah Detail Jadwal (PUT)
- **Method**       : `PUT`
- **URL**          : `/api/events/:id`
- **Deskripsi**    : Memperbarui judul, rincian, waktu, atau status skip agenda
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "title": "Evaluasi Proyek Mingguan (Update Ruangan)",
    "description": "Review sprint progres Q4 di Ruang Rapat Utama B",
    "start_time": "2026-11-10T10:00:00",
    "end_time": "2026-11-10T12:00:00",
    "is_skipped": false
  }
  ```
- **Response Sukses (200)**:
  ```json
  {
    "message": "Jadwal berhasil diperbarui",
    "data": {
      "event_id": 2,
      "title": "Evaluasi Proyek Mingguan (Update Ruangan)",
      "description": "Review sprint progres Q4 di Ruang Rapat Utama B",
      "start_time": "2026-11-10T10:00:00.000Z",
      "end_time": "2026-11-10T12:00:00.000Z",
      "is_skipped": false
    }
  }
  ```

#### 7. Menghapus Jadwal (DELETE)
- **Method**       : `DELETE`
- **URL**          : `/api/events/:id`
- **Deskripsi**    : Menghapus kegiatan dari kalender sistem (beserta cascading reminders)
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Jadwal dengan ID 9 berhasil dihapus",
    "deleted_event": {
      "event_id": 9,
      "title": "Sosialisasi Roadmap AI Nasional"
    }
  }
  ```

---

### D. Manajemen Grup & Kolaborasi (`/api/groups`)

#### 1. Mengambil Daftar Seluruh Grup
- **Method**       : `GET`
- **URL**          : `/api/groups`
- **Deskripsi**    : Menampilkan seluruh grup kolaborasi beserta jumlah anggotanya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar grup",
    "total": 7,
    "data": [
      {
        "group_id": 1,
        "group_name": "Tim Pengembang SIMAJU",
        "created_by": 1,
        "creator_name": "Alex Pratama, S.Kom.",
        "total_members": 2
      }
    ]
  }
  ```

#### 2. Mengambil Detail Grup & Anggota
- **Method**       : `GET`
- **URL**          : `/api/groups/:id`
- **Deskripsi**    : Menampilkan detail grup beserta daftar anggota di dalamnya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil detail grup",
    "data": {
      "group_id": 1,
      "group_name": "Tim Pengembang SIMAJU",
      "created_by": 1,
      "creator_name": "Alex Pratama, S.Kom.",
      "members": [
        {
          "user_id": 1,
          "name": "Alex Pratama, S.Kom.",
          "email": "alex@simaju.app",
          "instansi": "Pusat Riset Data"
        }
      ]
    }
  }
  ```

#### 3. Membuat Grup Baru
- **Method**       : `POST`
- **URL**          : `/api/groups`
- **Deskripsi**    : Membuat grup baru dan otomatis menjadikan pembuat sebagai anggota pertama
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "group_name": "Komite Transformasi Digital",
    "description": "Kelompok kerja akselerasi digitalisasi instansi",
    "created_by": 1
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Grup berhasil dibuat",
    "data": {
      "group_id": 8,
      "group_name": "Komite Transformasi Digital",
      "created_by": 1
    }
  }
  ```

#### 4. Menambahkan Anggota ke Grup
- **Method**       : `POST`
- **URL**          : `/api/groups/:id/members`
- **Deskripsi**    : Memasukkan pengguna ke dalam grup (relasi pivot `group_members`)
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "user_id": 3
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Pengguna berhasil ditambahkan ke grup",
    "data": {
      "group_id": 1,
      "user_id": 3
    }
  }
  ```

#### 5. Mengambil Jadwal Bersama Grup
- **Method**       : `GET`
- **URL**          : `/api/groups/:id/events`
- **Deskripsi**    : Menampilkan semua jadwal kegiatan bersama yang terkait dengan grup tertentu
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar jadwal untuk grup Tim Pengembang SIMAJU",
    "total": 1,
    "data": [
      {
        "event_id": 4,
        "title": "Presentasi Final Task Backend",
        "description": "Demo endpoint Vercel dan pengujian database relational",
        "start_time": "2026-11-10T10:00:00.000Z",
        "end_time": "2026-11-10T12:00:00.000Z",
        "is_skipped": false,
        "organizer_name": "Alex Pratama, S.Kom."
      }
    ]
  }
  ```

#### 6. Mengeluarkan Anggota dari Grup (DELETE)
- **Method**       : `DELETE`
- **URL**          : `/api/groups/:id/members/:userId`
- **Deskripsi**    : Menghapus keterikatan anggota dari suatu grup
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Pengguna dengan ID 3 berhasil dikeluarkan dari grup 1"
  }
  ```

---

### E. Manajemen Pengingat (`/api/reminders`)

#### 1. Mengambil Seluruh Pengingat
- **Method**       : `GET`
- **URL**          : `/api/reminders` (opsional filter: `?is_sent=false`)
- **Deskripsi**    : Mengambil daftar pengingat jadwal kegiatan beserta judul agenda dan pemiliknya
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar pengingat",
    "total": 2,
    "data": [
      {
        "reminder_id": 3,
        "event_id": 2,
        "event_title": "Evaluasi Proyek Mingguan",
        "event_start_time": "2026-11-03T14:00:00.000Z",
        "remind_at": "2026-11-03T13:45:00.000Z",
        "notification_type": "email",
        "is_sent": false,
        "user_name": "Alex Pratama, S.Kom."
      }
    ]
  }
  ```

#### 2. Membuat Pengingat Baru (POST)
- **Method**       : `POST`
- **URL**          : `/api/reminders`
- **Deskripsi**    : Menjadwalkan pengingat baru sebelum kegiatan berlangsung
- **Headers**      : `Content-Type: application/json`
- **Request Body** :
  ```json
  {
    "event_id": 2,
    "remind_at": "2026-11-10T09:45:00",
    "notification_type": "push_notification"
  }
  ```
- **Response Sukses (201)**:
  ```json
  {
    "message": "Pengingat berhasil dibuat",
    "data": {
      "reminder_id": 4,
      "event_id": 2,
      "remind_at": "2026-11-10T09:45:00.000Z",
      "notification_type": "push_notification",
      "is_sent": false
    }
  }
  ```

#### 3. Menandai Pengingat Terkirim (PATCH)
- **Method**       : `PATCH`
- **URL**          : `/api/reminders/:id/sent`
- **Deskripsi**    : Mengubah status pengingat menjadi sudah terkirim (`is_sent = true`)
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Pengingat berhasil ditandai sudah terkirim",
    "data": {
      "reminder_id": 3,
      "is_sent": true
    }
  }
  ```

#### 4. Menghapus Pengingat (DELETE)
- **Method**       : `DELETE`
- **URL**          : `/api/reminders/:id`
- **Deskripsi**    : Menghapus notifikasi pengingat dari basis data
- **Headers**      : *None*
- **Request Body** : *None*
- **Response Sukses (200)**:
  ```json
  {
    "message": "Pengingat dengan ID 4 berhasil dihapus",
    "deleted_reminder": {
      "reminder_id": 4,
      "event_id": 2
    }
  }
  ```

---

## Menjalankan Secara Lokal

### Prasyarat
- Node.js versi 18 ke atas
- Database PostgreSQL (Lokal atau Cloud Neon.tech / Supabase)

### Langkah Instalasi
1. Clone repositori dan masuk ke direktori proyek:
   ```bash
   git clone https://github.com/misaelsammy/simaju-backend.git
   cd simaju-backend
   ```

2. Pasang dependensi:
   ```bash
   npm install
   ```

3. Salin konfigurasi environment:
   ```bash
   cp .env.example .env
   ```
   Atur nilai `DATABASE_URL` pada file `.env` dengan kredensial PostgreSQL Anda.

4. Inisialisasi skema tabel dan data awal:
   ```bash
   npm run db:init
   npm run db:seed
   ```

5. Jalankan server lokal:
   ```bash
   npm run dev
   ```
   Server aktif dan dapat diakses di `http://localhost:3000`.

---

## Pengujian API

Seluruh endpoint telah dipetakan ke dalam format Postman Collection v2.1.0 lengkap dengan contoh request dan response:
- File koleksi: [`SIMAJU API.postman_collection.json`](./SIMAJU%20API.postman_collection.json) atau [`simaju_api_collection.json`](./simaju_api_collection.json)
- Kompatibel langsung dengan **Postman** maupun **Thunder Client** (VS Code).
- Dilengkapi dengan 5 folder modul (`00. Root & Health`, `01. Users & Preferences`, `02. Events & Schedules`, `03. Groups & Collaboration`, `04. Reminders & Notifications`), dokumentasi parameter, serta 47 contoh saved response (200 OK, 201 Created, 400 Bad Request, 404 Not Found).
- Variabel bawaan `{{base_url}}` sudah otomatis mengarah ke URL produksi Vercel (`https://simaju-backend.vercel.app`).
