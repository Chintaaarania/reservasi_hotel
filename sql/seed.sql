
USE db_reservasi_hotel;

-- 1. Data Admin
INSERT INTO users
(username, password_hash, nama_lengkap, role)
VALUES
(
    'admin',
    'scrypt:32768:8:1$gYx39bT42BwYI1y9$88f1176bc5a6d5bb9611b4142f31a2bd2beae7d4a41d91cd4a0e28f14a6dc6d7b42fbb1b938f3cb2a1d2932fcd4cfec2b32258fa4d9d10e6e73775b1129bc2bb',
    'Administrator Utama',
    'admin'
);

-- 2. Profil Hotel
INSERT INTO profil_hotel
(nama_hotel, alamat, nomor_telepon, email, deskripsi)
VALUES
(
    'Grand Blue Resort & Hotel',
    'Jl. Pantai Utama No. 88, Bali',
    '0361-9876543',
    'info@grandblue.com',
    'Hotel bintang 4 dengan pemandangan laut dan pelayanan eksklusif.'
);

-- 3. Tipe Kamar
INSERT INTO tipe_kamar
(nama_tipe, deskripsi, harga_per_malam, kapasitas)
VALUES
('Standard Room', 'Kamar minimalis modern dengan tempat tidur Queen Size', 450000, 2),
('Superior Room', 'Kamar nyaman dengan pemandangan kebun hotel', 650000, 2),
('Deluxe Room', 'Kamar luas dengan balkon pribadi dan pemandangan laut', 950000, 2),
('Executive Suite', 'Suite mewah dengan ruang tamu terpisah', 1800000, 4);

-- 4. Fasilitas
INSERT INTO fasilitas (nama_fasilitas, keterangan)
VALUES
('Free Wi-Fi High Speed', 'Akses Wi-Fi hingga 100 Mbps'),
('Air Conditioner (AC)', 'Sistem pendingin ruangan'),
('Smart TV 50 Inch', 'TV dengan akses hiburan digital'),
('Kamar Mandi Dalam', 'Shower air hangat dan perlengkapan mandi'),
('Mini Bar & Kulkas', 'Kulkas kecil dengan minuman dingin'),
('Balkon / Teras', 'Balkon menghadap laut atau taman');

-- 5. Relasi Tipe Kamar dan Fasilitas
INSERT INTO kamar_fasilitas (tipe_kamar_id, fasilitas_id)
VALUES
(1,1), (1,2), (1,4),
(2,1), (2,2), (2,3), (2,4),
(3,1), (3,2), (3,3), (3,4), (3,5), (3,6),
(4,1), (4,2), (4,3), (4,4), (4,5), (4,6);

-- 6. Data Kamar
INSERT INTO kamar (nomor_kamar, tipe_kamar_id, status)
VALUES
('101', 1, 'tersedia'),
('102', 1, 'tersedia'),
('201', 2, 'tersedia'),
('202', 2, 'pemeliharaan'),
('301', 3, 'tersedia'),
('401', 4, 'tersedia');

-- 7. Data Tamu
INSERT INTO tamu
(nik_paspor, nama_lengkap, email, nomor_telepon, alamat)
VALUES
('3171010203040001', 'Hendra Wijaya', 'hendra@gmail.com', '081234567890', 'Jl. Melati No. 12, Jakarta'),
('3171010203040002', 'Siti Rahma', 'siti@yahoo.com', '085678901234', 'Jl. Mawar No. 45, Bandung');

-- 8. Layanan Tambahan
INSERT INTO layanan (nama_layanan, harga)
VALUES
('Extra Bed', 150000),
('Laundry Express', 50000),
('Antar Jemput Bandara', 200000),
('Breakfast Buffet', 75000);
