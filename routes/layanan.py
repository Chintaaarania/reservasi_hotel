from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

layanan_bp = Blueprint('layanan', __name__)

@layanan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    layanan_list = db.session.execute(db.text("SELECT * FROM layanan ORDER BY id DESC")).fetchall()
    return render_template('layanan/index.html', layanan_list=layanan_list)

@layanan_bp.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(
        db.text("INSERT INTO layanan (nama_layanan, harga) VALUES (:nama, :harga)"),
        {'nama': request.form.get('nama_layanan'), 'harga': request.form.get('harga')}
    )
    db.session.commit()
    flash('Layanan tambahan berhasil ditambahkan!', 'success')
    return redirect(url_for('layanan.index'))

@layanan_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(db.text("DELETE FROM layanan WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Layanan berhasil dihapus!', 'warning')
    return redirect(url_for('layanan.index'))