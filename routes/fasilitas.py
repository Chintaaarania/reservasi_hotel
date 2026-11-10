from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

fasilitas_bp = Blueprint('fasilitas', __name__)

def get_clean_fasilitas():
    raw_data = firebase_db.reference('fasilitas').get()
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

@fasilitas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    fasilitas_list = get_clean_fasilitas()
    fasilitas_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)

    return render_template('fasilitas/index.html', fasilitas_list=fasilitas_list)

@fasilitas_bp.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    nama = request.form.get('nama_fasilitas')
    keterangan = request.form.get('keterangan')

    ref = firebase_db.reference('fasilitas')
    new_ref = ref.push()
    new_ref.set({
        'id': new_ref.key,
        'nama_fasilitas': nama,
        'keterangan': keterangan
    })

    flash('Fasilitas berhasil ditambahkan!', 'success')
    return redirect(url_for('fasilitas.index'))

@fasilitas_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    firebase_db.reference(f'fasilitas/{id}').delete()
    flash('Fasilitas berhasil dihapus!', 'warning')
    return redirect(url_for('fasilitas.index'))