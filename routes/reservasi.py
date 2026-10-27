from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from services.reservasi_service import buat_reservasi

reservasi_bp = Blueprint('reservasi', __name__)

@reservasi_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_list = db.session.execute(db.text("""
        SELECT r.*, t.nama_lengkap AS nama_tamu, k.nomor_kamar 
        FROM reservasi r
        JOIN tamu t ON r.tamu_id = t.id
        JOIN kamar k ON r.kamar_id = k.id
        ORDER BY r.id DESC
    """)).fetchall()
    return render_template('reservasi/index.html', reservasi_list=reservasi_list)

@reservasi_bp.route('/buat', methods=['GET', 'POST'])
def buat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        tamu_id = request.form.get('tamu_id')
        kamar_id = request.form.get('kamar_id')
        checkin = request.form.get('tanggal_checkin')
        checkout = request.form.get('tanggal_checkout')
        user_id = session['user_id']

        sukses, pesan = buat_reservasi(tamu_id, kamar_id, checkin, checkout, user_id)
        if sukses:
            flash(pesan, 'success')
            return redirect(url_for('reservasi.index'))
        else:
            flash(pesan, 'danger')

    tamu_list = db.session.execute(db.text("SELECT * FROM tamu")).fetchall()
    kamar_list = db.session.execute(db.text("""
        SELECT k.*, tk.nama_tipe, tk.harga_per_malam 
        FROM kamar k 
        JOIN tipe_kamar tk ON k.tipe_kamar_id = tk.id 
        WHERE k.status = 'tersedia'
    """)).fetchall()

    return render_template('reservasi/create.html', tamu_list=tamu_list, kamar_list=kamar_list)

@reservasi_bp.route('/detail/<int:id>')
def detail(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi = db.session.execute(db.text("""
        SELECT r.*, t.nama_lengkap AS nama_tamu, t.nomor_telepon, k.nomor_kamar, tk.nama_tipe
        FROM reservasi r
        JOIN tamu t ON r.tamu_id = t.id
        JOIN kamar k ON r.kamar_id = k.id
        JOIN tipe_kamar tk ON k.tipe_kamar_id = tk.id
        WHERE r.id = :id
    """), {'id': id}).fetchone()

    return render_template('reservasi/detail.html', reservasi=reservasi)