from database import db

def proses_pembayaran(reservasi_id, metode_pembayaran, jumlah_bayar, status_pembayaran):
    try:
        db.session.execute(
            db.text("""
                INSERT INTO pembayaran (reservasi_id, metode_pembayaran, jumlah_bayar, status_pembayaran)
                VALUES (:res_id, :metode, :jumlah, :status)
            """),
            {
                'res_id': reservasi_id,
                'metode': metode_pembayaran,
                'jumlah': jumlah_bayar,
                'status': status_pembayaran
            }
        )
        db.session.commit()
        return True, "Pembayaran berhasil dicatat."
    except Exception as e:
        db.session.rollback()
        return False, f"Gagal mencatat pembayaran: {str(e)}"