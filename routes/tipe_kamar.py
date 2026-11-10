import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from firebase_admin import db as firebase_db

tipe_kamar_bp = Blueprint('tipe_kamar', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_clean_tipe():
    raw_data = firebase_db.reference('tipe_kamar').get()
    items = []
    if not raw_data:
        return items
    if isinstance(raw_data, dict):
        for key, value in raw_data.items():
            if isinstance(value, dict):
                val_copy = value.copy()
                val_copy['id'] = val_copy.get('id', key)
                items.append(val_copy)
    elif isinstance(raw_data, list):
        for idx, item in enumerate(raw_data):
            if isinstance(item, dict):
                item_copy = item.copy()
                item_copy['id'] = item_copy.get('id', idx)
                items.append(item_copy)
    return items

@tipe_kamar_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe_list = get_clean_tipe()
    tipe_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
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
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Upload dilewati di environment serverless: {e}')
                    gambar_name = 'default_kamar.jpg' 

        ref = firebase_db.reference('tipe_kamar')
        new_ref = ref.push()
        new_ref.set({
            'id': new_ref.key,
            'nama_tipe': request.form.get('nama_tipe'),
            'harga_per_malam': request.form.get('harga_per_malam'),
            'kapasitas': request.form.get('kapasitas'),
            'deskripsi': request.form.get('deskripsi'),
            'gambar': gambar_name
        })

        flash('Tipe kamar berhasil ditambahkan!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Tambah')

@tipe_kamar_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe = firebase_db.reference(f'tipe_kamar/{id}').get() or {}

    if request.method == 'POST':
        # Default awal pakai gambar lama
        gambar_name = tipe.get('gambar', 'default_kamar.jpg')

        # 1. Prioritaskan URL gambar dari input teks jika diisi
        gambar_url_input = request.form.get('gambar_url')
        if gambar_url_input and gambar_url_input.strip() != '':
            gambar_name = gambar_url_input.strip()

        # 2. Cek jika mengunggah file fisik lokal
        elif 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Upload dilewati di serverless: {e}')
                    # Pada Vercel, jika upload file fisik ditolak serverless, simpan nama file
                    gambar_name = filename

        # Update data ke Firebase
        firebase_db.reference(f'tipe_kamar/{id}').update({
            'nama_tipe': request.form.get('nama_tipe'),
            'harga_per_malam': request.form.get('harga_per_malam'),
            'kapasitas': request.form.get('kapasitas'),
            'deskripsi': request.form.get('deskripsi'),
            'gambar': gambar_name
        })

        flash('Tipe kamar berhasil diperbarui!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Edit', tipe=tipe)

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe = firebase_db.reference(f'tipe_kamar/{id}').get() or {}

    if request.method == 'POST':
        # 1. Pertahankan gambar lama sebagai default awal
        gambar_name = tipe.get('gambar', 'default_kamar.jpg')

        # 2. Cek jika user memasukkan URL gambar langsung melalui form
        if request.form.get('gambar_url'):
            gambar_name = request.form.get('gambar_url')

        # 3. Cek jika user mengunggah file fisik
        elif 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Simpan file lokal dilewati di Vercel Serverless: {e}')
                    # Di serverless, jika file tidak bisa disimpan ke disk, 
                    # kita tetap bisa menyimpan nama filename-nya atau URL-nya
                    gambar_name = filename

        # 4. Update data di Firebase Realtime Database
        update_data = {
            'nama_tipe': request.form.get('nama_tipe'),
            'harga_per_malam': request.form.get('harga_per_malam'),
            'kapasitas': request.form.get('kapasitas'),
            'deskripsi': request.form.get('deskripsi'),
            'gambar': gambar_name
        }

        firebase_db.reference(f'tipe_kamar/{id}').update(update_data)

        flash('Tipe kamar berhasil diperbarui!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Edit', tipe=tipe)
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe = firebase_db.reference(f'tipe_kamar/{id}').get() or {}

    if request.method == 'POST':
        gambar_name = tipe.get('gambar', 'default_kamar.jpg')

        if 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                try:
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    gambar_name = filename
                except Exception as e:
                    current_app.logger.warning(f'Upload dilewati di serverless: {e}')

        firebase_db.reference(f'tipe_kamar/{id}').update({
            'nama_tipe': request.form.get('nama_tipe'),
            'harga_per_malam': request.form.get('harga_per_malam'),
            'kapasitas': request.form.get('kapasitas'),
            'deskripsi': request.form.get('deskripsi'),
            'gambar': gambar_name
        })

        flash('Tipe kamar berhasil diperbarui!', 'success')
        return redirect(url_for('tipe_kamar.index'))

    return render_template('tipe_kamar/form.html', action='Edit', tipe=tipe)

@tipe_kamar_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    firebase_db.reference(f'tipe_kamar/{id}').delete()
    flash('Tipe kamar berhasil dihapus!', 'warning')
    return redirect(url_for('tipe_kamar.index'))