from database import db

def cari_kamar_kosong(tipe_kamar_id, checkin, checkout):
    sql = """
        SELECT k.*, tk.nama_tipe, tk.harga_per_malam 
        FROM kamar k
        JOIN tipe_kamar tk ON k.tipe_kamar_id = tk.id
        WHERE k.status = 'tersedia'
    """
    params = {'checkin': checkin, 'checkout': checkout}

    if tipe_kamar_id:
        sql += " AND k.tipe_kamar_id = :tipe_id"
        params['tipe_id'] = tipe_kamar_id

    sql += """
        AND k.id NOT IN (
            SELECT kamar_id FROM reservasi
            WHERE status_reservasi IN ('booking', 'checkin')
              AND NOT (tanggal_checkout <= :checkin OR tanggal_checkin >= :checkout)
        )
        ORDER BY k.nomor_kamar ASC
    """

    kamar_tersedia = db.session.execute(db.text(sql), params).fetchall()
    return kamar_tersedia