
CREATE DATABASE IF NOT EXISTS db_reservasi_hotel;
USE db_reservasi_hotel;

-- 1. Tabel Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    role ENUM('admin', 'resepsionis', 'manajer')
        NOT NULL DEFAULT 'resepsionis',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel Tipe Kamar
CREATE TABLE IF NOT EXISTS tipe_kamar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_tipe VARCHAR(50) NOT NULL,
    harga_per_malam DECIMAL(12,2) NOT NULL,
    kapasitas INT NOT NULL,
    deskripsi TEXT
);

-- 3. Tabel Fasilitas
CREATE TABLE IF NOT EXISTS fasilitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_fasilitas VARCHAR(100) NOT NULL,
    keterangan VARCHAR(255)
);

-- 4. Tabel Kamar
CREATE TABLE IF NOT EXISTS kamar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_kamar VARCHAR(10) UNIQUE NOT NULL,
    tipe_kamar_id INT NOT NULL,
    status ENUM('tersedia', 'terisi', 'pemeliharaan', 'kotor')
        DEFAULT 'tersedia',
    FOREIGN KEY (tipe_kamar_id)
        REFERENCES tipe_kamar(id) ON DELETE CASCADE
);

-- 5. Tabel Relasi Kamar dan Fasilitas
CREATE TABLE IF NOT EXISTS kamar_fasilitas (
    tipe_kamar_id INT NOT NULL,
    fasilitas_id INT NOT NULL,
    PRIMARY KEY (tipe_kamar_id, fasilitas_id),
    FOREIGN KEY (tipe_kamar_id)
        REFERENCES tipe_kamar(id) ON DELETE CASCADE,
    FOREIGN KEY (fasilitas_id)
        REFERENCES fasilitas(id) ON DELETE CASCADE
);

-- 6. Tabel Tamu
CREATE TABLE IF NOT EXISTS tamu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nik_paspor VARCHAR(30) UNIQUE NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    nomor_telepon VARCHAR(20) NOT NULL,
    alamat TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabel Reservasi
CREATE TABLE IF NOT EXISTS reservasi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_reservasi VARCHAR(20) UNIQUE NOT NULL,
    tamu_id INT NOT NULL,
    kamar_id INT NOT NULL,
    tanggal_checkin DATE NOT NULL,
    tanggal_checkout DATE NOT NULL,
    total_malam INT NOT NULL,
    total_harga DECIMAL(12,2) NOT NULL,
    status_reservasi ENUM(
        'booking', 'checkin', 'checkout', 'batal'
    ) DEFAULT 'booking',
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tamu_id) REFERENCES tamu(id),
    FOREIGN KEY (kamar_id) REFERENCES kamar(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 8. Tabel Layanan
CREATE TABLE IF NOT EXISTS layanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_layanan VARCHAR(100) NOT NULL,
    harga DECIMAL(12,2) NOT NULL
);

-- 9. Tabel Detail Layanan Reservasi
CREATE TABLE IF NOT EXISTS detail_layanan_reservasi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservasi_id INT NOT NULL,
    layanan_id INT NOT NULL,
    jumlah INT DEFAULT 1,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservasi_id)
        REFERENCES reservasi(id) ON DELETE CASCADE,
    FOREIGN KEY (layanan_id) REFERENCES layanan(id)
);

-- 10. Tabel Pembayaran
CREATE TABLE IF NOT EXISTS pembayaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservasi_id INT NOT NULL,
    metode_pembayaran ENUM(
        'tunai', 'transfer', 'kartu_kredit', 'qris'
    ) NOT NULL,
    jumlah_bayar DECIMAL(12,2) NOT NULL,
    status_pembayaran ENUM('dp', 'lunas') NOT NULL,
    tanggal_bayar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservasi_id) REFERENCES reservasi(id)
);

-- 11. Tabel Activity Log
CREATE TABLE IF NOT EXISTS activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    aktivitas VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 12. Tabel Profil Hotel
CREATE TABLE IF NOT EXISTS profil_hotel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_hotel VARCHAR(150) NOT NULL,
    alamat TEXT,
    nomor_telepon VARCHAR(20),
    email VARCHAR(100),
    deskripsi TEXT
);
