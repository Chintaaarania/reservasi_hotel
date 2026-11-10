from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

tamu_bp = Blueprint('tamu', __name__)

def get_clean_tamu():
    raw_data = firebase_db.reference('tamu').get()
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

@tamu_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    tamu_list = get_clean_tamu()
    tamu_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
    return render_template('tamu/index.html', tamu_list=tamu_list)

@tamu_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        ref = firebase_db.reference('tamu')
        new_ref = ref.push()
        new_ref.set({
            'id': new_ref.key,
            'nik_paspor': request.form.get('nik_paspor'),
            'nama_lengkap': request.form.get('nama_lengkap'),
            'email': request.form.get('email'),
            'nomor_telepon': request.form.get('nomor_telepon'),
            'alamat': request.form.get('alamat')
        })

        flash('Data tamu berhasil ditambahkan!', 'success')
        return redirect(url_for('tamu.index'))

    return render_template('tamu/form.html', action='Tambah')

@tamu_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tamu = firebase_db.reference(f'tamu/{id}').get()
    
    if request.method == 'POST':
        firebase_db.reference(f'tamu/{id}').update({
            'nik_paspor': request.form.get('nik_paspor'),
            'nama_lengkap': request.form.get('nama_lengkap'),
            'email': request.form.get('email'),
            'nomor_telepon': request.form.get('nomor_telepon'),
            'alamat': request.form.get('alamat')
        })
        flash('Data tamu berhasil diperbarui!', 'success')
        return redirect(url_for('tamu.index'))

    return render_template('tamu/form.html', action='Edit', tamu=tamu)

@tamu_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    firebase_db.reference(f'tamu/{id}').delete()
    flash('Data tamu berhasil dihapus!', 'warning')
    return redirect(url_for('tamu.index'))