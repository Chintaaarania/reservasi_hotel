import uuid
from datetime import datetime
from database import db

def hitung_total_biaya(kamar_id, checkin_str, checkout_str):
    date_format = "%Y-%m-%d"
    checkin = datetime.strptime(checkin_str, date_format)
    checkout = datetime.strptime(checkout_str, date_format)
    
    total_malam = (checkout - checkin).days
    if total_malam <= 0:
        return 0, 0, "Tanggal check-out harus setelah check-in."

    row = db.session.execute(
        db.text("SELECT tk.harga_per_malam FROM kamar k JOIN tipe_kamar tk ON k.tipe_kamar_id = tk.id WHERE k.id = :id"),
        {'id': kamar_id}
    ).fetchone()

    if not row:
        return 0, 0, "Kamar tidak ditemukan."

    harga_per_malam = float(row.harga_per_malam)
    total_harga = total_malam * harga_per_malam

    return total_malam, total_harga, None

def buat_reservasi(tamu_id, kamar_id, checkin, checkout, user_id):
    total_malam, total_harga, err = hitung_total_biaya(kamar_id, checkin, checkout)
    if err:
        return False, err

    # Cek bentrok jadwal (overbooking)
    bentrok = db.session.execute(
        db.text("""
            SELECT id FROM reservasi
            WHERE kamar_id = :kamar_id
              AND status_reservasi IN ('booking', 'checkin')
              AND NOT (tanggal_checkout <= :checkin OR tanggal_checkin >= :checkout)
        """),
        {'kamar_id': kamar_id, 'checkin': checkin, 'checkout': checkout}
    ).fetchone()

    if bentrok:
        return False, "Kamar sudah dipesan pada tanggal tersebut."

    kode_reservasi = f"RES-{uuid.uuid4().hex[:8].upper()}"

    db.session.execute(
        db.text("""
            INSERT INTO reservasi (kode_reservasi, tamu_id, kamar_id, tanggal_checkin, tanggal_checkout, total_malam, total_harga, status_reservasi, user_id)
            VALUES (:kode, :tamu, :kamar, :checkin, :checkout, :malam, :harga, 'booking', :user)
        """),
        {
            'kode': kode_reservasi,
            'tamu': tamu_id,
            'kamar': kamar_id,
            'checkin': checkin,
            'checkout': checkout,
            'malam': total_malam,
            'harga': total_harga,
            'user': user_id
        }
    )
    
    # Log Aktivitas
    db.session.execute(
        db.text("INSERT INTO activity_log (user_id, aktivitas) VALUES (:user, :act)"),
        {'user': user_id, 'act': f"Membuat reservasi {kode_reservasi}"}
    )

    db.session.commit()
    return True, f"Reservasi berhasil dibuat dengan kode: {kode_reservasi}"