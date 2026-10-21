from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

checkin_checkout_bp = Blueprint('checkin_checkout', __name__)

@checkin_checkout_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_list = db.session.execute(db.text("""
        SELECT r.*, t.nama_lengkap AS nama_tamu, k.nomor_kamar 
        FROM reservasi r
        JOIN tamu t ON r.tamu_id = t.id
        JOIN kamar k ON r.kamar_id = k.id
        WHERE r.status_reservasi IN ('booking', 'checkin')
        ORDER BY r.tanggal_checkin ASC
    """)).fetchall()

    return render_template('checkin_checkout/index.html', reservasi_list=reservasi_list)

@checkin_checkout_bp.route('/checkin/<int:id>', methods=['POST'])
def checkin(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(
        db.text("UPDATE reservasi SET status_reservasi = 'checkin' WHERE id = :id"),
        {'id': id}
    )
    db.session.execute(
        db.text("UPDATE kamar SET status = 'terisi' WHERE id = (SELECT kamar_id FROM reservasi WHERE id = :id)"),
        {'id': id}
    )
    db.session.commit()
    flash('Proses Check-In berhasil!', 'success')
    return redirect(url_for('checkin_checkout.index'))

@checkin_checkout_bp.route('/checkout/<int:id>', methods=['POST'])
def checkout(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(
        db.text("UPDATE reservasi SET status_reservasi = 'checkout' WHERE id = :id"),
        {'id': id}
    )
    db.session.execute(
        db.text("UPDATE kamar SET status = 'kotor' WHERE id = (SELECT kamar_id FROM reservasi WHERE id = :id)"),
        {'id': id}
    )
    db.session.commit()
    flash('Proses Check-Out berhasil! Status kamar menjadi kotor.', 'info')
    return redirect(url_for('checkin_checkout.index'))