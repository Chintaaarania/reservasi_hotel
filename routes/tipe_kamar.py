from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

tipe_kamar_bp = Blueprint('tipe_kamar', __name__)

@tipe_kamar_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe_list = db.session.execute(db.text("SELECT * FROM tipe_kamar ORDER BY id DESC")).fetchall()
    return render_template('tipe_kamar/index.html', tipe_list=tipe_list)

@tipe_kamar_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        db.session.execute(
            db.text("""
                INSERT INTO tipe_kamar (nama_tipe, harga_per_malam, kapasitas, deskripsi)
                VALUES (:nama, :harga, :kapasitas, :deskripsi)
            """),
            {
                'nama': request.form.get('nama_tipe'),
                'harga': request.form.get('harga_per_malam'),
                'kapasitas': request.form.get('kapasitas'),
                'deskripsi': request.form.get('deskripsi')
            }
        )
        db.session.commit()
        flash('Tipe kamar berhasil ditambahkan!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Tambah')

@tipe_kamar_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe = db.session.execute(db.text("SELECT * FROM tipe_kamar WHERE id = :id"), {'id': id}).fetchone()

    if request.method == 'POST':
        db.session.execute(
            db.text("""
                UPDATE tipe_kamar SET nama_tipe=:nama, harga_per_malam=:harga, 
                kapasitas=:kapasitas, deskripsi=:deskripsi WHERE id=:id
            """),
            {
                'nama': request.form.get('nama_tipe'),
                'harga': request.form.get('harga_per_malam'),
                'kapasitas': request.form.get('kapasitas'),
                'deskripsi': request.form.get('deskripsi'),
                'id': id
            }
        )
        db.session.commit()
        flash('Tipe kamar berhasil diperbarui!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Edit', tipe=tipe)

@tipe_kamar_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(db.text("DELETE FROM tipe_kamar WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Tipe kamar berhasil dihapus!', 'warning')
    return redirect(url_for('tipe_kamar.index'))