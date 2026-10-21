from database import db

def dapatkan_laporan_pendapatan(start_date=None, end_date=None):
    sql = """
        SELECT p.id, p.tanggal_bayar, r.kode_reservasi, t.nama_lengkap AS nama_tamu,
               p.metode_pembayaran, p.status_pembayaran, p.jumlah_bayar
        FROM pembayaran p
        JOIN reservasi r ON p.reservasi_id = r.id
        JOIN tamu t ON r.tamu_id = t.id
        WHERE 1=1
    """
    params = {}

    if start_date:
        sql += " AND DATE(p.tanggal_bayar) >= :start_date"
        params['start_date'] = start_date

    if end_date:
        sql += " AND DATE(p.tanggal_bayar) <= :end_date"
        params['end_date'] = end_date

    sql += " ORDER BY p.tanggal_bayar DESC"

    laporan = db.session.execute(db.text(sql), params).fetchall()
    
    total_pendapatan = sum(row.jumlah_bayar for row in laporan) if laporan else 0

    return laporan, total_pendapatan