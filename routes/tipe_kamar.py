import base64
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
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
        gambar_name = 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800'
        
        gambar_url_input = request.form.get('gambar_url')
        gambar_base64_input = request.form.get('gambar_base64')

        if gambar_url_input and gambar_url_input.strip() != '':
            gambar_name = gambar_url_input.strip()
        elif gambar_base64_input and gambar_base64_input.strip() != '':
            gambar_name = gambar_base64_input.strip()

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

    # Ambil data dari Firebase
    ref = firebase_db.reference('tipe_kamar')
    all_tipe = ref.get()
    
    tipe = None
    target_key = id

    if isinstance(all_tipe, dict):
        if id in all_tipe:
            tipe = all_tipe[id]
        else:
            for k, v in all_tipe.items():
                if isinstance(v, dict) and str(v.get('id')) == str(id):
                    tipe = v
                    target_key = k
                    break
    elif isinstance(all_tipe, list):
        for idx, item in enumerate(all_tipe):
            if isinstance(item, dict) and str(item.get('id', idx)) == str(id):
                tipe = item
                target_key = str(idx)
                break

    if request.method == 'POST':
        gambar_name = tipe.get('gambar') if tipe else 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800'

        gambar_url_input = request.form.get('gambar_url')
        gambar_base64_input = request.form.get('gambar_base64')

        if gambar_url_input and gambar_url_input.strip() != '':
            gambar_name = gambar_url_input.strip()
        elif gambar_base64_input and gambar_base64_input.strip() != '':
            gambar_name = gambar_base64_input.strip()

        update_payload = {
            'nama_tipe': request.form.get('nama_tipe'),
            'harga_per_malam': request.form.get('harga_per_malam'),
            'kapasitas': request.form.get('kapasitas'),
            'deskripsi': request.form.get('deskripsi'),
            'gambar': gambar_name
        }

        # Update node Firebase secara langsung
        firebase_db.reference(f'tipe_kamar/{target_key}').update(update_payload)

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