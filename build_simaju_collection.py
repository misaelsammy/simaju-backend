#!/usr/bin/env python3
import json

collection = {
    "info": {
        "_postman_id": "b3e94a50-25e1-4c6e-82e7-f1388d019f6a",
        "name": "SIMAJU REST API",
        "description": "Koleksi endpoint REST API untuk Proyek SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu).\nMencakup modul: Root & Health, Users & Preferences, Events & Schedules, Groups & Collaboration, serta Reminders & Notifications.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "variable": [
        {
            "key": "base_url",
            "value": "https://simaju-backend.vercel.app"
        }
    ],
    "item": []
}

def make_header(content_type="application/json"):
    if content_type:
        return [{"key": "Content-Type", "value": content_type}]
    return []

def make_response_headers():
    return [
        {"key": "content-type", "value": "application/json; charset=utf-8"},
        {"key": "server", "value": "Vercel"},
        {"key": "cache-control", "value": "public, max-age=0, must-revalidate"}
    ]

def make_url(path, query_params=None, path_vars=None):
    clean_path = path.strip("/")
    path_segments = [p for p in clean_path.split("/") if p]
    
    raw = "{{base_url}}" + ("/" + clean_path if clean_path else "/")
    
    url_obj = {
        "raw": raw,
        "host": ["{{base_url}}"],
        "path": path_segments
    }
    
    if query_params:
        url_obj["query"] = [{"key": k, "value": str(v)} for k, v in query_params.items()]
        query_str = "&".join([f"{k}={v}" for k, v in query_params.items()])
        url_obj["raw"] += f"?{query_str}"
        
    if path_vars:
        url_obj["variable"] = [{"key": k, "value": str(v)} for k, v in path_vars.items()]
        
    return url_obj

def make_example_response(name, status_code, status_text, req_method, req_url, body_dict):
    body_str = json.dumps(body_dict, indent=2, ensure_ascii=False)
    return {
        "name": f"{status_code} - {name}",
        "originalRequest": {
            "method": req_method,
            "header": make_header() if req_method in ["POST", "PUT", "PATCH"] else [],
            "url": req_url
        },
        "status": status_text,
        "code": status_code,
        "_postman_previewlanguage": "json",
        "header": make_response_headers(),
        "cookie": [],
        "body": body_str
    }

# ==========================================
# 00. Root & Health
# ==========================================
root_folder = {
    "name": "00. Root & Health",
    "item": [
        {
            "name": "Root — GET /",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/"),
                "description": "Deskripsi: Cek endpoint root dan status serverless REST API SIMAJU.\n\nResponse Sukses (200):\n{\n  \"success\": true,\n  \"message\": \"SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu) REST API is running successfully\",\n  \"version\": \"1.0.0\",\n  \"endpoints\": {\n    \"users\": \"/api/users\",\n    \"events\": \"/api/events\",\n    \"groups\": \"/api/groups\",\n    \"reminders\": \"/api/reminders\"\n  },\n  \"timestamp\": \"2026-10-25T09:31:48.866Z\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/"), {
                    "success": True,
                    "message": "SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu) REST API is running successfully",
                    "version": "1.0.0",
                    "endpoints": {
                        "users": "/api/users",
                        "events": "/api/events",
                        "groups": "/api/groups",
                        "reminders": "/api/reminders"
                    },
                    "timestamp": "2026-10-25T09:31:48.866Z"
                })
            ]
        }
    ]
}

# ==========================================
# 01. Users & Preferences
# ==========================================
users_folder = {
    "name": "01. Users & Preferences",
    "item": [
        {
            "name": "List Users — GET /api/users",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/users"),
                "description": "Deskripsi: Mengambil seluruh daftar pengguna SIMAJU beserta instansi dan preferensi default.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar pengguna\",\n  \"total\": 6,\n  \"data\": [\n    {\n      \"user_id\": 1,\n      \"name\": \"Alex Pratama, S.Kom.\",\n      \"email\": \"alex@simaju.app\",\n      \"instansi\": \"Pusat Riset Data\",\n      \"default_reminder_minutes\": 30,\n      \"theme\": \"system\"\n    }\n  ]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/users"), {
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
                        },
                        {
                            "user_id": 2,
                            "name": "Bella Safira, M.T.",
                            "email": "bella@simaju.app",
                            "instansi": "Direktorat Tata Kelola TI",
                            "default_reminder_minutes": 15,
                            "theme": "light"
                        }
                    ]
                })
            ]
        },
        {
            "name": "Detail User Profile — GET /api/users/:id",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/users/:id", path_vars={"id": "1"}),
                "description": "Deskripsi: Mengambil detail profil pengguna berdasarkan ID termasuk preferensi tema dan default waktu pengingat.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil profil pengguna\",\n  \"data\": {\n    \"user_id\": 1,\n    \"name\": \"Alex Pratama, S.Kom.\",\n    \"email\": \"alex@simaju.app\",\n    \"instansi\": \"Pusat Riset Data\",\n    \"default_reminder_minutes\": 30,\n    \"theme\": \"system\"\n  }\n}\n\nResponse Error (404):\n{\n  \"error\": \"Pengguna dengan ID 999 tidak ditemukan\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/users/:id", path_vars={"id": "1"}), {
                    "message": "Berhasil mengambil profil pengguna",
                    "data": {
                        "user_id": 1,
                        "name": "Alex Pratama, S.Kom.",
                        "email": "alex@simaju.app",
                        "instansi": "Pusat Riset Data",
                        "default_reminder_minutes": 30,
                        "theme": "system"
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "GET", make_url("/api/users/:id", path_vars={"id": "999"}), {
                    "error": "Pengguna dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Register User — POST /api/users/register",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "name": "Citra Dewi",
                        "email": "citra.dewi@simaju.app",
                        "password": "Password123!",
                        "instansi": "Biro Perencanaan dan Keuangan",
                        "default_reminder_minutes": 15,
                        "theme": "light"
                    }, indent=2)
                },
                "url": make_url("/api/users/register"),
                "description": "Deskripsi: Mendaftarkan akun pengguna baru ke dalam SIMAJU sekaligus membuat entri pengaturan preferensi pengguna.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"name\": \"Citra Dewi\",\n  \"email\": \"citra.dewi@simaju.app\",\n  \"password\": \"Password123!\",\n  \"instansi\": \"Biro Perencanaan dan Keuangan\",\n  \"default_reminder_minutes\": 15,\n  \"theme\": \"light\"\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Registrasi pengguna berhasil\",\n  \"data\": {\n    \"user_id\": 7,\n    \"name\": \"Citra Dewi\",\n    \"email\": \"citra.dewi@simaju.app\",\n    \"instansi\": \"Biro Perencanaan dan Keuangan\"\n  }\n}\n\nResponse Error (400):\n{\n  \"error\": \"Email sudah terdaftar dalam sistem\"\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/users/register"), {
                    "message": "Registrasi pengguna berhasil",
                    "data": {
                        "user_id": 7,
                        "name": "Citra Dewi",
                        "email": "citra.dewi@simaju.app",
                        "instansi": "Biro Perencanaan dan Keuangan"
                    }
                }),
                make_example_response("Email Exists", 400, "Bad Request", "POST", make_url("/api/users/register"), {
                    "error": "Email sudah terdaftar dalam sistem"
                }),
                make_example_response("Missing Fields", 400, "Bad Request", "POST", make_url("/api/users/register"), {
                    "error": "Field name, email, dan password wajib diisi"
                })
            ]
        },
        {
            "name": "Login User — POST /api/users/login",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "email": "alex@simaju.app",
                        "password": "hashed_pass_alex"
                    }, indent=2)
                },
                "url": make_url("/api/users/login"),
                "description": "Deskripsi: Melakukan otentikasi akun pengguna dengan memverifikasi email dan password.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"email\": \"alex@simaju.app\",\n  \"password\": \"hashed_pass_alex\"\n}\n\nResponse Sukses (200):\n{\n  \"message\": \"Login berhasil\",\n  \"data\": {\n    \"user_id\": 1,\n    \"name\": \"Alex Pratama, S.Kom.\",\n    \"email\": \"alex@simaju.app\",\n    \"instansi\": \"Pusat Riset Data\"\n  }\n}\n\nResponse Error (400):\n{\n  \"error\": \"Kredensial login tidak valid\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "POST", make_url("/api/users/login"), {
                    "message": "Login berhasil",
                    "data": {
                        "user_id": 1,
                        "name": "Alex Pratama, S.Kom.",
                        "email": "alex@simaju.app",
                        "instansi": "Pusat Riset Data"
                    }
                }),
                make_example_response("Invalid Credentials", 400, "Bad Request", "POST", make_url("/api/users/login"), {
                    "error": "Kredensial login tidak valid"
                }),
                make_example_response("User Not Found", 404, "Not Found", "POST", make_url("/api/users/login"), {
                    "error": "Pengguna dengan email tersebut tidak ditemukan"
                })
            ]
        },
        {
            "name": "Update User Profile — PUT /api/users/:id",
            "request": {
                "method": "PUT",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "name": "Alex Pratama, M.Kom.",
                        "instansi": "Pusat Riset Data Nasional",
                        "default_reminder_minutes": 45,
                        "theme": "dark"
                    }, indent=2)
                },
                "url": make_url("/api/users/:id", path_vars={"id": "1"}),
                "description": "Deskripsi: Memperbarui nama, instansi, atau pengaturan preferensi tema & pengingat pengguna.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"name\": \"Alex Pratama, M.Kom.\",\n  \"instansi\": \"Pusat Riset Data Nasional\",\n  \"default_reminder_minutes\": 45,\n  \"theme\": \"dark\"\n}\n\nResponse Sukses (200):\n{\n  \"message\": \"Profil dan preferensi pengguna berhasil diperbarui\",\n  \"data\": {\n    \"user_id\": 1,\n    \"name\": \"Alex Pratama, M.Kom.\",\n    \"email\": \"alex@simaju.app\",\n    \"instansi\": \"Pusat Riset Data Nasional\",\n    \"default_reminder_minutes\": 45,\n    \"theme\": \"dark\"\n  }\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "PUT", make_url("/api/users/:id", path_vars={"id": "1"}), {
                    "message": "Profil dan preferensi pengguna berhasil diperbarui",
                    "data": {
                        "user_id": 1,
                        "name": "Alex Pratama, M.Kom.",
                        "email": "alex@simaju.app",
                        "instansi": "Pusat Riset Data Nasional",
                        "default_reminder_minutes": 45,
                        "theme": "dark"
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "PUT", make_url("/api/users/:id", path_vars={"id": "999"}), {
                    "error": "Pengguna dengan ID 999 tidak ditemukan"
                })
            ]
        }
    ]
}

# ==========================================
# 02. Events & Schedules
# ==========================================
events_folder = {
    "name": "02. Events & Schedules",
    "item": [
        {
            "name": "List Events — GET /api/events",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/events"),
                "description": "Deskripsi: Mengambil semua daftar jadwal kegiatan (lengkap dengan data user, grup, dan pola recurring).\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar jadwal kegiatan\",\n  \"total\": 8,\n  \"data\": [\n    {\n      \"event_id\": 2,\n      \"user_id\": 1,\n      \"user_name\": \"Alex Pratama, S.Kom.\",\n      \"group_id\": null,\n      \"group_name\": null,\n      \"pattern_id\": 1,\n      \"recurring_frequency\": \"weekly\",\n      \"title\": \"Evaluasi Proyek Mingguan\",\n      \"start_time\": \"2026-11-03T14:00:00.000Z\",\n      \"end_time\": \"2026-11-03T16:00:00.000Z\",\n      \"is_skipped\": false\n    }\n  ]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/events"), {
                    "message": "Berhasil mengambil daftar jadwal kegiatan",
                    "total": 8,
                    "data": [
                        {
                            "event_id": 2,
                            "user_id": 1,
                            "user_name": "Alex Pratama, S.Kom.",
                            "group_id": None,
                            "group_name": None,
                            "pattern_id": 1,
                            "recurring_frequency": "weekly",
                            "title": "Evaluasi Proyek Mingguan",
                            "description": "Review sprint progres Q4 di Ruang Rapat Utama A",
                            "start_time": "2026-11-03T14:00:00.000Z",
                            "end_time": "2026-11-03T16:00:00.000Z",
                            "is_skipped": False
                        }
                    ]
                })
            ]
        },
        {
            "name": "Filter Events by Date & User — GET /api/events",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/events", query_params={"user_id": "1", "start_date": "2026-11-01", "end_date": "2026-11-30"}),
                "description": "Deskripsi: Memfilter jadwal kegiatan berdasarkan ID pengguna dan rentang tanggal.\n\nQuery Parameters:\n- `user_id`: ID pengguna (integer)\n- `start_date`: Tanggal awal (YYYY-MM-DD)\n- `end_date`: Tanggal akhir (YYYY-MM-DD)\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar jadwal kegiatan\",\n  \"total\": 3,\n  \"data\": [...]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/events", query_params={"user_id": "1", "start_date": "2026-11-01", "end_date": "2026-11-30"}), {
                    "message": "Berhasil mengambil daftar jadwal kegiatan",
                    "total": 3,
                    "data": [
                        {
                            "event_id": 2,
                            "user_id": 1,
                            "user_name": "Alex Pratama, S.Kom.",
                            "title": "Evaluasi Proyek Mingguan",
                            "start_time": "2026-11-03T14:00:00.000Z",
                            "end_time": "2026-11-03T16:00:00.000Z"
                        }
                    ]
                })
            ]
        },
        {
            "name": "Check Schedule Conflict — GET /api/events/check-conflict",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/events/check-conflict", query_params={"user_id": "1", "start_time": "2026-11-10T09:00:00", "end_time": "2026-11-10T11:00:00"}),
                "description": "Deskripsi: Pengecekan overlap / bentrok jadwal untuk pengguna tertentu pada rentang waktu yang dipilih.\n\nQuery Parameters:\n- `user_id`: ID pengguna\n- `start_time`: Waktu mulai (ISO-8601)\n- `end_time`: Waktu selesai (ISO-8601)\n\nResponse Sukses (200 - Konflik Ditemukan):\n{\n  \"message\": \"Pengecekan konflik selesai\",\n  \"data\": {\n    \"has_conflict\": true,\n    \"conflict_count\": 1,\n    \"conflicts\": [\n      {\n        \"event_id\": 4,\n        \"title\": \"Presentasi Final Task Backend\",\n        \"start_time\": \"2026-11-10T10:00:00.000Z\",\n        \"end_time\": \"2026-11-10T12:00:00.000Z\"\n      }\n    ]\n  }\n}"
            },
            "response": [
                make_example_response("Conflict Detected", 200, "OK", "GET", make_url("/api/events/check-conflict", query_params={"user_id": "1", "start_time": "2026-11-10T09:00:00", "end_time": "2026-11-10T11:00:00"}), {
                    "message": "Pengecekan konflik selesai",
                    "data": {
                        "has_conflict": True,
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
                }),
                make_example_response("No Conflict", 200, "OK", "GET", make_url("/api/events/check-conflict", query_params={"user_id": "1", "start_time": "2026-12-01T08:00:00", "end_time": "2026-12-01T09:00:00"}), {
                    "message": "Pengecekan konflik selesai",
                    "data": {
                        "has_conflict": False,
                        "conflict_count": 0,
                        "conflicts": []
                    }
                })
            ]
        },
        {
            "name": "Detail Event — GET /api/events/:id",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/events/:id", path_vars={"id": "2"}),
                "description": "Deskripsi: Mengambil detail lengkap jadwal kegiatan beserta daftar notifikasi pengingat (reminders) terkait.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil detail jadwal\",\n  \"data\": {\n    \"event_id\": 2,\n    \"user_id\": 1,\n    \"user_name\": \"Alex Pratama, S.Kom.\",\n    \"title\": \"Evaluasi Proyek Mingguan\",\n    \"start_time\": \"2026-11-03T14:00:00.000Z\",\n    \"end_time\": \"2026-11-03T16:00:00.000Z\",\n    \"reminders\": [\n      {\n        \"reminder_id\": 3,\n        \"remind_at\": \"2026-11-03T13:45:00.000Z\",\n        \"notification_type\": \"email\",\n        \"is_sent\": false\n      }\n    ]\n  }\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/events/:id", path_vars={"id": "2"}), {
                    "message": "Berhasil mengambil detail jadwal",
                    "data": {
                        "event_id": 2,
                        "user_id": 1,
                        "user_name": "Alex Pratama, S.Kom.",
                        "user_email": "alex@simaju.app",
                        "group_id": None,
                        "group_name": None,
                        "pattern_id": 1,
                        "recurring_frequency": "weekly",
                        "recurring_end_date": "2026-12-31",
                        "title": "Evaluasi Proyek Mingguan",
                        "description": "Review sprint progres Q4 di Ruang Rapat Utama A",
                        "start_time": "2026-11-03T14:00:00.000Z",
                        "end_time": "2026-11-03T16:00:00.000Z",
                        "is_skipped": False,
                        "reminders": [
                            {
                                "reminder_id": 3,
                                "remind_at": "2026-11-03T13:45:00.000Z",
                                "notification_type": "email",
                                "is_sent": False
                            }
                        ]
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "GET", make_url("/api/events/:id", path_vars={"id": "999"}), {
                    "error": "Jadwal dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Create Event — POST /api/events",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "user_id": 1,
                        "title": "Sosialisasi Roadmap AI Nasional",
                        "description": "Pembahasan implementasi roadmap kecerdasan buatan terpadu",
                        "start_time": "2026-12-05T09:00:00",
                        "end_time": "2026-12-05T11:30:00",
                        "allow_conflict": True
                    }, indent=2)
                },
                "url": make_url("/api/events"),
                "description": "Deskripsi: Membuat jadwal kegiatan mandiri baru. Dilengkapi validasi konflik jadwal (opsional `allow_conflict: true`).\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"user_id\": 1,\n  \"title\": \"Sosialisasi Roadmap AI Nasional\",\n  \"description\": \"Pembahasan implementasi roadmap kecerdasan buatan terpadu\",\n  \"start_time\": \"2026-12-05T09:00:00\",\n  \"end_time\": \"2026-12-05T11:30:00\",\n  \"allow_conflict\": true\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Jadwal berhasil ditambahkan\",\n  \"data\": {\n    \"event_id\": 9,\n    \"user_id\": 1,\n    \"title\": \"Sosialisasi Roadmap AI Nasional\",\n    \"start_time\": \"2026-12-05T09:00:00.000Z\",\n    \"end_time\": \"2026-12-05T11:30:00.000Z\"\n  }\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/events"), {
                    "message": "Jadwal berhasil ditambahkan",
                    "data": {
                        "event_id": 9,
                        "user_id": 1,
                        "group_id": None,
                        "pattern_id": None,
                        "title": "Sosialisasi Roadmap AI Nasional",
                        "description": "Pembahasan implementasi roadmap kecerdasan buatan terpadu",
                        "start_time": "2026-12-05T09:00:00.000Z",
                        "end_time": "2026-12-05T11:30:00.000Z",
                        "is_skipped": False
                    }
                }),
                make_example_response("Conflict Error", 400, "Bad Request", "POST", make_url("/api/events"), {
                    "error": "Jadwal bertabrakan dengan kegiatan lain yang sudah ada. Gunakan allow_conflict: true jika tetap ingin menambahkan.",
                    "conflicts": [
                        {
                            "event_id": 4,
                            "title": "Presentasi Final Task Backend",
                            "start_time": "2026-11-10T10:00:00.000Z",
                            "end_time": "2026-11-10T12:00:00.000Z"
                        }
                    ]
                }),
                make_example_response("Missing Fields", 400, "Bad Request", "POST", make_url("/api/events"), {
                    "error": "Field user_id, title, start_time, dan end_time wajib diisi"
                })
            ]
        },
        {
            "name": "Create Recurring Event — POST /api/events",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "user_id": 1,
                        "title": "Rapat Koordinasi Rutin Divisi IT",
                        "description": "Sinkronisasi sprint mingguan",
                        "start_time": "2026-12-01T13:00:00",
                        "end_time": "2026-12-01T14:30:00",
                        "frequency": "weekly",
                        "end_date": "2026-12-31",
                        "allow_conflict": True
                    }, indent=2)
                },
                "url": make_url("/api/events"),
                "description": "Deskripsi: Membuat jadwal kegiatan berulang (recurring event) dengan pola frekuensi (`daily`, `weekly`, `monthly`) dan tanggal berakhir pola.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"user_id\": 1,\n  \"title\": \"Rapat Koordinasi Rutin Divisi IT\",\n  \"description\": \"Sinkronisasi sprint mingguan\",\n  \"start_time\": \"2026-12-01T13:00:00\",\n  \"end_time\": \"2026-12-01T14:30:00\",\n  \"frequency\": \"weekly\",\n  \"end_date\": \"2026-12-31\",\n  \"allow_conflict\": true\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Jadwal berhasil ditambahkan\",\n  \"data\": {\n    \"event_id\": 10,\n    \"pattern_id\": 2,\n    \"title\": \"Rapat Koordinasi Rutin Divisi IT\"\n  }\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/events"), {
                    "message": "Jadwal berhasil ditambahkan",
                    "data": {
                        "event_id": 10,
                        "user_id": 1,
                        "group_id": None,
                        "pattern_id": 2,
                        "title": "Rapat Koordinasi Rutin Divisi IT",
                        "description": "Sinkronisasi sprint mingguan",
                        "start_time": "2026-12-01T13:00:00.000Z",
                        "end_time": "2026-12-01T14:30:00.000Z",
                        "is_skipped": False
                    }
                })
            ]
        },
        {
            "name": "Update Event — PUT /api/events/:id",
            "request": {
                "method": "PUT",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "title": "Evaluasi Proyek Mingguan (Update Ruangan)",
                        "description": "Review sprint progres Q4 di Ruang Rapat Utama B",
                        "start_time": "2026-11-10T10:00:00",
                        "end_time": "2026-11-10T12:00:00",
                        "is_skipped": False
                    }, indent=2)
                },
                "url": make_url("/api/events/:id", path_vars={"id": "2"}),
                "description": "Deskripsi: Memperbarui data judul, deskripsi, waktu mulai/selesai, atau status skip jadwal.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"title\": \"Evaluasi Proyek Mingguan (Update Ruangan)\",\n  \"description\": \"Review sprint progres Q4 di Ruang Rapat Utama B\",\n  \"start_time\": \"2026-11-10T10:00:00\",\n  \"end_time\": \"2026-11-10T12:00:00\",\n  \"is_skipped\": false\n}\n\nResponse Sukses (200):\n{\n  \"message\": \"Jadwal berhasil diperbarui\",\n  \"data\": {\n    \"event_id\": 2,\n    \"title\": \"Evaluasi Proyek Mingguan (Update Ruangan)\"\n  }\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "PUT", make_url("/api/events/:id", path_vars={"id": "2"}), {
                    "message": "Jadwal berhasil diperbarui",
                    "data": {
                        "event_id": 2,
                        "user_id": 1,
                        "title": "Evaluasi Proyek Mingguan (Update Ruangan)",
                        "description": "Review sprint progres Q4 di Ruang Rapat Utama B",
                        "start_time": "2026-11-10T10:00:00.000Z",
                        "end_time": "2026-11-10T12:00:00.000Z",
                        "is_skipped": False
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "PUT", make_url("/api/events/:id", path_vars={"id": "999"}), {
                    "error": "Jadwal dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Delete Event — DELETE /api/events/:id",
            "request": {
                "method": "DELETE",
                "header": [],
                "url": make_url("/api/events/:id", path_vars={"id": "999"}),
                "description": "Deskripsi: Menghapus jadwal kegiatan dari sistem (beserta pengingat cascading terkait).\n\nResponse Sukses (200):\n{\n  \"message\": \"Jadwal dengan ID 9 berhasil dihapus\",\n  \"deleted_event\": {\n    \"event_id\": 9,\n    \"title\": \"Sosialisasi Roadmap AI Nasional\"\n  }\n}\n\nResponse Error (404):\n{\n  \"error\": \"Jadwal dengan ID 999 tidak ditemukan\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "DELETE", make_url("/api/events/:id", path_vars={"id": "9"}), {
                    "message": "Jadwal dengan ID 9 berhasil dihapus",
                    "deleted_event": {
                        "event_id": 9,
                        "title": "Sosialisasi Roadmap AI Nasional"
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "DELETE", make_url("/api/events/:id", path_vars={"id": "999"}), {
                    "error": "Jadwal dengan ID 999 tidak ditemukan"
                })
            ]
        }
    ]
}

# ==========================================
# 03. Groups & Collaboration
# ==========================================
groups_folder = {
    "name": "03. Groups & Collaboration",
    "item": [
        {
            "name": "List Groups — GET /api/groups",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/groups"),
                "description": "Deskripsi: Mengambil seluruh daftar grup kolaborasi kerja beserta informasi creator dan jumlah anggota.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar grup\",\n  \"total\": 7,\n  \"data\": [\n    {\n      \"group_id\": 1,\n      \"group_name\": \"Tim Pengembang SIMAJU\",\n      \"created_by\": 1,\n      \"creator_name\": \"Alex Pratama, S.Kom.\",\n      \"total_members\": 2\n    }\n  ]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/groups"), {
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
                })
            ]
        },
        {
            "name": "Detail Group — GET /api/groups/:id",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/groups/:id", path_vars={"id": "1"}),
                "description": "Deskripsi: Mengambil detail grup beserta daftar lengkap anggota di dalam grup tersebut.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil detail grup\",\n  \"data\": {\n    \"group_id\": 1,\n    \"group_name\": \"Tim Pengembang SIMAJU\",\n    \"created_by\": 1,\n    \"creator_name\": \"Alex Pratama, S.Kom.\",\n    \"members\": [\n      {\n        \"user_id\": 1,\n        \"name\": \"Alex Pratama, S.Kom.\",\n        \"email\": \"alex@simaju.app\",\n        \"instansi\": \"Pusat Riset Data\"\n      }\n    ]\n  }\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/groups/:id", path_vars={"id": "1"}), {
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
                            },
                            {
                                "user_id": 2,
                                "name": "Bella Safira, M.T.",
                                "email": "bella@simaju.app",
                                "instansi": "Direktorat Tata Kelola TI"
                            }
                        ]
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "GET", make_url("/api/groups/:id", path_vars={"id": "999"}), {
                    "error": "Grup dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Create Group — POST /api/groups",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "group_name": "Komite Transformasi Digital",
                        "description": "Kelompok kerja akselerasi digitalisasi instansi",
                        "created_by": 1
                    }, indent=2)
                },
                "url": make_url("/api/groups"),
                "description": "Deskripsi: Membuat grup kerja baru dan secara otomatis mendaftarkan pembuatnya sebagai anggota pertama.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"group_name\": \"Komite Transformasi Digital\",\n  \"description\": \"Kelompok kerja akselerasi digitalisasi instansi\",\n  \"created_by\": 1\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Grup berhasil dibuat\",\n  \"data\": {\n    \"group_id\": 8,\n    \"group_name\": \"Komite Transformasi Digital\",\n    \"created_by\": 1\n  }\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/groups"), {
                    "message": "Grup berhasil dibuat",
                    "data": {
                        "group_id": 8,
                        "group_name": "Komite Transformasi Digital",
                        "description": "Kelompok kerja akselerasi digitalisasi instansi",
                        "created_by": 1
                    }
                }),
                make_example_response("Missing Fields", 400, "Bad Request", "POST", make_url("/api/groups"), {
                    "error": "Field group_name dan created_by wajib diisi"
                })
            ]
        },
        {
            "name": "Add Group Member — POST /api/groups/:id/members",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "user_id": 3
                    }, indent=2)
                },
                "url": make_url("/api/groups/:id/members", path_vars={"id": "1"}),
                "description": "Deskripsi: Menambahkan pengguna ke dalam grup kolaborasi kerja.\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"user_id\": 3\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Pengguna berhasil ditambahkan ke grup\",\n  \"data\": {\n    \"group_id\": 1,\n    \"user_id\": 3\n  }\n}\n\nResponse Error (400):\n{\n  \"error\": \"Pengguna sudah menjadi anggota grup ini\"\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/groups/:id/members", path_vars={"id": "1"}), {
                    "message": "Pengguna berhasil ditambahkan ke grup",
                    "data": {
                        "group_id": 1,
                        "user_id": 3
                    }
                }),
                make_example_response("Already Member", 400, "Bad Request", "POST", make_url("/api/groups/:id/members", path_vars={"id": "1"}), {
                    "error": "Pengguna sudah menjadi anggota grup ini"
                }),
                make_example_response("Group Not Found", 404, "Not Found", "POST", make_url("/api/groups/:id/members", path_vars={"id": "999"}), {
                    "error": "Grup dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Group Shared Events — GET /api/groups/:id/events",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/groups/:id/events", path_vars={"id": "1"}),
                "description": "Deskripsi: Mengambil semua jadwal kegiatan bersama yang diasosiasikan dengan grup tertentu.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar jadwal untuk grup Tim Pengembang SIMAJU\",\n  \"total\": 1,\n  \"data\": [\n    {\n      \"event_id\": 4,\n      \"title\": \"Presentasi Final Task Backend\",\n      \"start_time\": \"2026-11-10T10:00:00.000Z\",\n      \"end_time\": \"2026-11-10T12:00:00.000Z\"\n    }\n  ]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/groups/:id/events", path_vars={"id": "1"}), {
                    "message": "Berhasil mengambil daftar jadwal untuk grup Tim Pengembang SIMAJU",
                    "total": 1,
                    "data": [
                        {
                            "event_id": 4,
                            "title": "Presentasi Final Task Backend",
                            "description": "Demo endpoint Vercel dan pengujian database relational",
                            "start_time": "2026-11-10T10:00:00.000Z",
                            "end_time": "2026-11-10T12:00:00.000Z",
                            "is_skipped": False,
                            "organizer_name": "Alex Pratama, S.Kom."
                        }
                    ]
                }),
                make_example_response("Not Found", 404, "Not Found", "GET", make_url("/api/groups/:id/events", path_vars={"id": "999"}), {
                    "error": "Grup dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Remove Group Member — DELETE /api/groups/:id/members/:userId",
            "request": {
                "method": "DELETE",
                "header": [],
                "url": make_url("/api/groups/:id/members/:userId", path_vars={"id": "1", "userId": "3"}),
                "description": "Deskripsi: Mengeluarkan anggota tertentu dari grup kolaborasi.\n\nResponse Sukses (200):\n{\n  \"message\": \"Pengguna dengan ID 3 berhasil dikeluarkan dari grup 1\"\n}\n\nResponse Error (404):\n{\n  \"error\": \"Anggota tidak ditemukan di grup tersebut\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "DELETE", make_url("/api/groups/:id/members/:userId", path_vars={"id": "1", "userId": "3"}), {
                    "message": "Pengguna dengan ID 3 berhasil dikeluarkan dari grup 1"
                }),
                make_example_response("Not Found", 404, "Not Found", "DELETE", make_url("/api/groups/:id/members/:userId", path_vars={"id": "1", "userId": "999"}), {
                    "error": "Anggota tidak ditemukan di grup tersebut"
                })
            ]
        }
    ]
}

# ==========================================
# 04. Reminders & Notifications
# ==========================================
reminders_folder = {
    "name": "04. Reminders & Notifications",
    "item": [
        {
            "name": "List Reminders — GET /api/reminders",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/reminders"),
                "description": "Deskripsi: Mengambil seluruh daftar pengingat jadwal kegiatan beserta judul kegiatan dan nama pemiliknya.\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar pengingat\",\n  \"total\": 2,\n  \"data\": [\n    {\n      \"reminder_id\": 3,\n      \"event_id\": 2,\n      \"event_title\": \"Evaluasi Proyek Mingguan\",\n      \"remind_at\": \"2026-11-03T13:45:00.000Z\",\n      \"notification_type\": \"email\",\n      \"is_sent\": false\n    }\n  ]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/reminders"), {
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
                            "is_sent": False,
                            "user_name": "Alex Pratama, S.Kom."
                        }
                    ]
                })
            ]
        },
        {
            "name": "Upcoming Reminders — GET /api/reminders",
            "request": {
                "method": "GET",
                "header": [],
                "url": make_url("/api/reminders", query_params={"is_sent": "false"}),
                "description": "Deskripsi: Memfilter notifikasi pengingat yang belum terkirim (`is_sent = false`).\n\nQuery Parameters:\n- `is_sent`: Status pengiriman pengingat (boolean: true / false)\n\nResponse Sukses (200):\n{\n  \"message\": \"Berhasil mengambil daftar pengingat\",\n  \"total\": 2,\n  \"data\": [...]\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "GET", make_url("/api/reminders", query_params={"is_sent": "false"}), {
                    "message": "Berhasil mengambil daftar pengingat",
                    "total": 2,
                    "data": [
                        {
                            "reminder_id": 3,
                            "event_id": 2,
                            "event_title": "Evaluasi Proyek Mingguan",
                            "remind_at": "2026-11-03T13:45:00.000Z",
                            "notification_type": "email",
                            "is_sent": False
                        }
                    ]
                })
            ]
        },
        {
            "name": "Create Reminder — POST /api/reminders",
            "request": {
                "method": "POST",
                "header": make_header(),
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({
                        "event_id": 2,
                        "remind_at": "2026-11-10T09:45:00",
                        "notification_type": "push_notification"
                    }, indent=2)
                },
                "url": make_url("/api/reminders"),
                "description": "Deskripsi: Menambahkan pengingat baru untuk suatu jadwal kegiatan (tipe: `email`, `push_notification`, `sms`).\n\nHeaders: Content-Type: application/json\n\nRequest Body:\n{\n  \"event_id\": 2,\n  \"remind_at\": \"2026-11-10T09:45:00\",\n  \"notification_type\": \"push_notification\"\n}\n\nResponse Sukses (201):\n{\n  \"message\": \"Pengingat berhasil dibuat\",\n  \"data\": {\n    \"reminder_id\": 4,\n    \"event_id\": 2,\n    \"remind_at\": \"2026-11-10T09:45:00.000Z\",\n    \"notification_type\": \"push_notification\",\n    \"is_sent\": false\n  }\n}"
            },
            "response": [
                make_example_response("Created", 201, "Created", "POST", make_url("/api/reminders"), {
                    "message": "Pengingat berhasil dibuat",
                    "data": {
                        "reminder_id": 4,
                        "event_id": 2,
                        "remind_at": "2026-11-10T09:45:00.000Z",
                        "notification_type": "push_notification",
                        "is_sent": False
                    }
                }),
                make_example_response("Missing Fields", 400, "Bad Request", "POST", make_url("/api/reminders"), {
                    "error": "Field event_id dan remind_at wajib diisi"
                }),
                make_example_response("Event Not Found", 404, "Not Found", "POST", make_url("/api/reminders"), {
                    "error": "Jadwal dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Mark Reminder As Sent — PATCH /api/reminders/:id/sent",
            "request": {
                "method": "PATCH",
                "header": [],
                "url": make_url("/api/reminders/:id/sent", path_vars={"id": "3"}),
                "description": "Deskripsi: Menandai status pengingat telah terkirim (`is_sent = true`).\n\nResponse Sukses (200):\n{\n  \"message\": \"Pengingat berhasil ditandai sudah terkirim\",\n  \"data\": {\n    \"reminder_id\": 3,\n    \"is_sent\": true\n  }\n}\n\nResponse Error (404):\n{\n  \"error\": \"Pengingat dengan ID 999 tidak ditemukan\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "PATCH", make_url("/api/reminders/:id/sent", path_vars={"id": "3"}), {
                    "message": "Pengingat berhasil ditandai sudah terkirim",
                    "data": {
                        "reminder_id": 3,
                        "event_id": 2,
                        "remind_at": "2026-11-03T13:45:00.000Z",
                        "notification_type": "email",
                        "is_sent": True
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "PATCH", make_url("/api/reminders/:id/sent", path_vars={"id": "999"}), {
                    "error": "Pengingat dengan ID 999 tidak ditemukan"
                })
            ]
        },
        {
            "name": "Delete Reminder — DELETE /api/reminders/:id",
            "request": {
                "method": "DELETE",
                "header": [],
                "url": make_url("/api/reminders/:id", path_vars={"id": "999"}),
                "description": "Deskripsi: Menghapus data pengingat dari database.\n\nResponse Sukses (200):\n{\n  \"message\": \"Pengingat dengan ID 4 berhasil dihapus\",\n  \"deleted_reminder\": {\n    \"reminder_id\": 4,\n    \"event_id\": 2\n  }\n}\n\nResponse Error (404):\n{\n  \"error\": \"Pengingat dengan ID 999 tidak ditemukan\"\n}"
            },
            "response": [
                make_example_response("OK", 200, "OK", "DELETE", make_url("/api/reminders/:id", path_vars={"id": "4"}), {
                    "message": "Pengingat dengan ID 4 berhasil dihapus",
                    "deleted_reminder": {
                        "reminder_id": 4,
                        "event_id": 2
                    }
                }),
                make_example_response("Not Found", 404, "Not Found", "DELETE", make_url("/api/reminders/:id", path_vars={"id": "999"}), {
                    "error": "Pengingat dengan ID 999 tidak ditemukan"
                })
            ]
        }
    ]
}

collection["item"] = [
    root_folder,
    users_folder,
    events_folder,
    groups_folder,
    reminders_folder
]

# Write to "SIMAJU API.postman_collection.json"
with open("/home/ciel/Documents/simaju-backend/SIMAJU API.postman_collection.json", "w", encoding="utf-8") as f:
    json.dump(collection, f, indent=2, ensure_ascii=False)

print("Collection generated successfully!")
