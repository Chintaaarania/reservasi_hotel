USE db_reservasi_hotel;

-- User Admin Default (Username: admin, Password: admin123)
INSERT INTO users (nama, username, email, password_hash) VALUES
('Administrator Utama', 'admin', 'admin@hotel.com', 'scrypt:32768:8:1$gYx39bT42BwYI1y9$88f1176bc5a6d5bb9611b4142f31a2bd2beae7d4a41d91cd4a0e28f14a6dc6d7b42fbb1b938f3cb2a1d2932fcd4cfec2b32258fa4d9d10e6e73775b1129bc2bb');

-- Profil Hotel Initial
INSERT INTO profil_hotel (nama_hotel, alamat, nomor_telepon, email, deskripsi) VALUES
('Grand Blue Resort & Hotel', 'Jl. Pantai Utama No. 88, Bali', '0361-9876543', 'info@grandblue.com', 'Hotel bintang 4 dengan pemandangan laut dan pelayanan eksklusif.');

-- Tipe Kamar Initial
INSERT INTO tipe_kamar (nama_tipe, deskripsi, harga_per_malam, kapasitas) VALUES
('Standard Room', 'Kamar minimalis modern dengan tempat tidur Queen Size', 450000.00, 2),
('Superior Room', 'Kamar nyaman dengan pemandangan kebun hotel', 650000.00, 2),
('Deluxe Room', 'Kamar luas dengan balkon pribadi dan pemandangan laut', 950000.00, 2),
('Executive Suite', 'Suite mewah lengkap dengan area ruang tamu terpisah', 1800000.00, 4);

-- Fasilitas Initial
INSERT INTO fasilitas (nama_fasilitas, deskripsi) VALUES
('Free Wi-Fi High Speed', 'Akses Wi-Fi hingga 100 Mbps'),
('Air Conditioner (AC)', 'Sistem pendingin ruangan pintar'),
('Smart TV 50 Inch', 'Siaran TV satelit dan Netflix ready'),
('Kamar Mandi Dalam', 'Dengan shower air hangat dan perlengkapan mandi'),
('Mini Bar & Kulkas', 'Kulkas kecil dengan minuman dingin'),
('Balkon / Teras', 'Balkon menghadap laut atau taman');

-- Pemetaan Fasilitas
INSERT INTO fasilitas_tipe_kamar (tipe_kamar_id, fasilitas_id) VALUES
(1, 1), (1, 2), (1, 4),
(2, 1), (2, 2), (2, 3), (2, 4),
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6);

-- Data Kamar Initial
INSERT INTO kamar (nomor_kamar, tipe_kamar_id, lantai, status_kamar) VALUES
('101', 1, 1, 'Tersedia'),
('102', 1, 1, 'Tersedia'),
('201', 2, 2, 'Tersedia'),
('202', 2, 2, 'Dalam Perawatan'),
('301', 3, 3, 'Tersedia'),
('401', 4, 4, 'Tersedia');

-- Data Tamu Initial
INSERT INTO tamu (kode_tamu, nama_lengkap, jenis_identitas, nomor_identitas, nomor_telepon, email, alamat) VALUES
('TM-2026001', 'Hendra Wijaya', 'KTP', '3171010203040001', '081234567890', 'hendra@gmail.com', 'Jl. Melati No. 12, Jakarta'),
('TM-2026002', 'Siti Rahma', 'SIM', '0987654321', '085678901234', 'siti@yahoo.com', 'Jl. Mawar No. 45, Bandung');

-- Layanan Tambahan Initial
INSERT INTO layanan (nama_layanan, deskripsi, harga) VALUES
('Extra Bed', 'Kasur tambahan include sarapan', 150000.00),
('Laundry Express', 'Layanan cuci kilat per 5 kg', 50000.00),
('Antar Jemput Bandara', 'Layanan transportasi sekali jalan', 200000.00),
('Breakfast Buffet', 'Tambahan porsi sarapan', 75000.00);