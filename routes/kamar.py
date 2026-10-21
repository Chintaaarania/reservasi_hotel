from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

kamar_bp = Blueprint('kamar', __name__)

@kamar_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    kamar_list = db.session.execute(db.text("""
        SELECT k.*, t.nama_tipe, t.harga_per_malam 
        FROM kamar k 
        JOIN tipe_kamar t ON k.tipe_kamar_id = t.id 
        ORDER BY k.nomor_kamar ASC
    """)).fetchall()
    return render_template('kamar/index.html', kamar_list=kamar_list)

@kamar_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe_list = db.session.execute(db.text("SELECT * FROM tipe_kamar")).fetchall()

    if request.method == 'POST':
        nomor_kamar = request.form.get('nomor_kamar')
        tipe_kamar_id = request.form.get('tipe_kamar_id')
        status = request.form.get('status', 'tersedia')

        db.session.execute(
            db.text("INSERT INTO kamar (nomor_kamar, tipe_kamar_id, status) VALUES (:no, :tipe, :status)"),
            {'no': nomor_kamar, 'tipe': tipe_kamar_id, 'status': status}
        )
        db.session.commit()
        flash('Kamar berhasil ditambahkan!', 'success')
        return redirect(url_for('kamar.index'))

    return render_template('kamar/form.html', action='Tambah', tipe_list=tipe_list)

@kamar_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    kamar = db.session.execute(db.text("SELECT * FROM kamar WHERE id = :id"), {'id': id}).fetchone()
    tipe_list = db.session.execute(db.text("SELECT * FROM tipe_kamar")).fetchall()

    if request.method == 'POST':
        db.session.execute(
            db.text("UPDATE kamar SET nomor_kamar=:no, tipe_kamar_id=:tipe, status=:status WHERE id=:id"),
            {
                'no': request.form.get('nomor_kamar'),
                'tipe': request.form.get('tipe_kamar_id'),
                'status': request.form.get('status'),
                'id': id
            }
        )
        db.session.commit()
        flash('Data kamar berhasil diubah!', 'success')
        return redirect(url_for('kamar.index'))

    return render_template('kamar/form.html', action='Edit', kamar=kamar, tipe_list=tipe_list)

@kamar_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(db.text("DELETE FROM kamar WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Kamar berhasil dihapus!', 'warning')
    return redirect(url_for('kamar.index'))