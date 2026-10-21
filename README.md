# Sistem Reservasi Hotel (Flask + MySQL Laragon)

Aplikasi manajemen operasional hotel berbasis web yang dibangun menggunakan **Python Flask** dengan arsitektur **Blueprint + Service Layer Pattern** dan basis data **MySQL**.

---

## 🚀 Panduan Instalasi & Jalankan Aplikasi

### 1. Prasyarat Sistem
* **Laragon** (atau XAMPP) dengan layanan MySQL yang aktif.
* **Python 3.10+** sudah terpasang di sistem.

---

### 2. Pengaturan Database di Laragon
1. Buka **Laragon**, lalu jalankan service **MySQL**.
2. Buka **HeidiSQL** atau **phpMyAdmin**.
3. Jalankan skrip DDL SQL untuk membuat basis data dan tabel:
   * Import berkas `sql/schema.sql`
4. Masukkan data awal (*dummy data*):
   * Import berkas `sql/seed.sql`

---

### 3. Setup Virtual Environment & Dependensi
Buka terminal pada direktori proyek (`sistem_reservasi_hotel/`), lalu jalankan perintah berikut:

```bash
# Membuat Virtual Environment
python -m venv venv

# Aktivasi Virtual Environment (Windows)
venv\Scripts\activate

# Menginstal seluruh library yang dibutuhkan
pip install -r requirements.txt