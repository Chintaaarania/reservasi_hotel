from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from services.pembayaran_service import proses_pembayaran

pembayaran_bp = Blueprint('pembayaran', __name__)

@pembayaran_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    pembayaran_list = db.session.execute(db.text("""
        SELECT p.*, r.kode_reservasi, t.nama_lengkap AS nama_tamu
        FROM pembayaran p
        JOIN reservasi r ON p.reservasi_id = r.id
        JOIN tamu t ON r.tamu_id = t.id
        ORDER BY p.id DESC
    """)).fetchall()

    reservasi_pending = db.session.execute(db.text("""
        SELECT r.id, r.kode_reservasi, r.total_harga, t.nama_lengkap AS nama_tamu
        FROM reservasi r
        JOIN tamu t ON r.tamu_id = t.id
        WHERE r.id NOT IN (SELECT reservasi_id FROM pembayaran WHERE status_pembayaran = 'lunas')
    """)).fetchall()

    return render_template('pembayaran/index.html', pembayaran_list=pembayaran_list, reservasi_pending=reservasi_pending)

@pembayaran_bp.route('/bayar', methods=['POST'])
def bayar():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_id = request.form.get('reservasi_id')
    metode = request.form.get('metode_pembayaran')
    jumlah = request.form.get('jumlah_bayar')
    status = request.form.get('status_pembayaran')

    sukses, pesan = proses_pembayaran(reservasi_id, metode, jumlah, status)
    if sukses:
        flash(pesan, 'success')
    else:
        flash(pesan, 'danger')

    return redirect(url_for('pembayaran.index'))

@pembayaran_bp.route('/kwitansi/<int:id>')
def kwitansi(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    pembayaran = db.session.execute(db.text("""
        SELECT p.*, r.kode_reservasi, r.total_malam, r.tanggal_checkin, r.tanggal_checkout,
               t.nama_lengkap AS nama_tamu, k.nomor_kamar
        FROM pembayaran p
        JOIN reservasi r ON p.reservasi_id = r.id
        JOIN tamu t ON r.tamu_id = t.id
        JOIN kamar k ON r.kamar_id = k.id
        WHERE p.id = :id
    """), {'id': id}).fetchone()

    return render_template('pembayaran/kwitansi.html', pembayaran=pembayaran)