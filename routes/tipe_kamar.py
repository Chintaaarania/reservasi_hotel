import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from database import db

tipe_kamar_bp = Blueprint('tipe_kamar', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        gambar_name = 'default_kamar.jpg'
        
        if 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                
                # Lokasi penyimpanan mengacu ke folder static/uploads
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Upload dilewati di environment serverless: {e}')
                    gambar_name = 'default_kamar.jpg' 

        db.session.execute(
            db.text("""
                INSERT INTO tipe_kamar (nama_tipe, harga_per_malam, kapasitas, deskripsi, gambar)
                VALUES (:nama, :harga, :kapasitas, :deskripsi, :gambar)
            """),
            {
                'nama': request.form.get('nama_tipe'),
                'harga': request.form.get('harga_per_malam'),
                'kapasitas': request.form.get('kapasitas'),
                'deskripsi': request.form.get('deskripsi'),
                'gambar': gambar_name
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
        gambar_name = tipe.gambar

        if 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    
                    # Hapus gambar lama jika ada dan bukan default
                    if tipe.gambar and tipe.gambar != 'default_kamar.jpg':
                        old_path = os.path.join(upload_folder, tipe.gambar)
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except Exception:
                                pass
                                
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Upload dilewati di environment serverless: {e}')

        db.session.execute(
            db.text("""
                UPDATE tipe_kamar SET nama_tipe=:nama, harga_per_malam=:harga, 
                kapasitas=:kapasitas, deskripsi=:deskripsi, gambar=:gambar WHERE id=:id
            """),
            {
                'nama': request.form.get('nama_tipe'),
                'harga': request.form.get('harga_per_malam'),
                'kapasitas': request.form.get('kapasitas'),
                'deskripsi': request.form.get('deskripsi'),
                'gambar': gambar_name,
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

    tipe = db.session.execute(db.text("SELECT gambar FROM tipe_kamar WHERE id = :id"), {'id': id}).fetchone()
    if tipe and tipe.gambar and tipe.gambar != 'default_kamar.jpg':
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', tipe.gambar)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

    db.session.execute(db.text("DELETE FROM tipe_kamar WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Tipe kamar berhasil dihapus!', 'warning')
    return redirect(url_for('tipe_kamar.index'))