from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

tamu_bp = Blueprint('tamu', __name__)

@tamu_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    tamu_list = db.session.execute(db.text("SELECT * FROM tamu ORDER BY id DESC")).fetchall()
    return render_template('tamu/index.html', tamu_list=tamu_list)

@tamu_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nik_paspor = request.form.get('nik_paspor')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')
        nomor_telepon = request.form.get('nomor_telepon')
        alamat = request.form.get('alamat')

        db.session.execute(
            db.text("""
                INSERT INTO tamu (nik_paspor, nama_lengkap, email, nomor_telepon, alamat)
                VALUES (:nik, :nama, :email, :telp, :alamat)
            """),
            {'nik': nik_paspor, 'nama': nama_lengkap, 'email': email, 'telp': nomor_telepon, 'alamat': alamat}
        )
        db.session.commit()
        flash('Data tamu berhasil ditambahkan!', 'success')
        return redirect(url_for('tamu.index'))

    return render_template('tamu/form.html', action='Tambah')

@tamu_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tamu = db.session.execute(db.text("SELECT * FROM tamu WHERE id = :id"), {'id': id}).fetchone()
    
    if request.method == 'POST':
        db.session.execute(
            db.text("""
                UPDATE tamu SET nik_paspor=:nik, nama_lengkap=:nama, email=:email, 
                nomor_telepon=:telp, alamat=:alamat WHERE id=:id
            """),
            {
                'nik': request.form.get('nik_paspor'),
                'nama': request.form.get('nama_lengkap'),
                'email': request.form.get('email'),
                'telp': request.form.get('nomor_telepon'),
                'alamat': request.form.get('alamat'),
                'id': id
            }
        )
        db.session.commit()
        flash('Data tamu berhasil diperbarui!', 'success')
        return redirect(url_for('tamu.index'))

    return render_template('tamu/form.html', action='Edit', tamu=tamu)

@tamu_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db.session.execute(db.text("DELETE FROM tamu WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Data tamu berhasil dihapus!', 'warning')
    return redirect(url_for('tamu.index'))