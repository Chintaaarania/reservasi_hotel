
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

fasilitas_bp = Blueprint('fasilitas', __name__)

@fasilitas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    fasilitas_list = db.session.execute(
        db.text("SELECT * FROM fasilitas ORDER BY id DESC")
    ).fetchall()

    return render_template(
        'fasilitas/index.html',
        fasilitas_list=fasilitas_list
    )


@fasilitas_bp.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    nama = request.form.get('nama_fasilitas')
    keterangan = request.form.get('keterangan')

    db.session.execute(
        db.text("""
            INSERT INTO fasilitas (nama_fasilitas, keterangan)
            VALUES (:nama, :keterangan)
        """),
        {
            'nama': nama,
            'keterangan': keterangan
        }
    )

    db.session.commit()

    flash('Fasilitas berhasil ditambahkan!', 'success')

    return redirect(url_for('fasilitas.index'))


@fasilitas_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(
        db.text("DELETE FROM fasilitas WHERE id = :id"),
        {'id': id}
    )

    db.session.commit()

    flash('Fasilitas berhasil dihapus!', 'warning')

    return redirect(url_for('fasilitas.index'))
