from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

layanan_bp = Blueprint('layanan', __name__)

def get_clean_layanan():
    raw_data = firebase_db.reference('layanan').get()
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

@layanan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    layanan_list = get_clean_layanan()
    layanan_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
    return render_template('layanan/index.html', layanan_list=layanan_list)

@layanan_bp.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    ref = firebase_db.reference('layanan')
    new_ref = ref.push()
    new_ref.set({
        'id': new_ref.key,
        'nama_layanan': request.form.get('nama_layanan'),
        'harga': request.form.get('harga')
    })

    flash('Layanan tambahan berhasil ditambahkan!', 'success')
    return redirect(url_for('layanan.index'))

@layanan_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    firebase_db.reference(f'layanan/{id}').delete()
    flash('Layanan berhasil dihapus!', 'warning')
    return redirect(url_for('layanan.index'))