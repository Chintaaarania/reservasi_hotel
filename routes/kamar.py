from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

kamar_bp = Blueprint('kamar', __name__)

def get_clean_data(ref_name):
    raw_data = firebase_db.reference(ref_name).get()
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

@kamar_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    kamar_raw = get_clean_data('kamar')
    tipe_raw = {str(t.get('id')): t for t in get_clean_data('tipe_kamar')}

    kamar_list = []
    for k in kamar_raw:
        t_info = tipe_raw.get(str(k.get('tipe_kamar_id')), {})
        k['nama_tipe'] = t_info.get('nama_tipe', '-')
        k['harga_per_malam'] = t_info.get('harga_per_malam', 0)
        kamar_list.append(k)

    kamar_list.sort(key=lambda x: str(x.get('nomor_kamar', '')))
    return render_template('kamar/index.html', kamar_list=kamar_list)

@kamar_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe_list = get_clean_data('tipe_kamar')

    if request.method == 'POST':
        nomor_kamar = request.form.get('nomor_kamar')
        tipe_kamar_id = request.form.get('tipe_kamar_id')
        status = request.form.get('status', 'tersedia')

        ref = firebase_db.reference('kamar')
        new_ref = ref.push()
        new_ref.set({
            'id': new_ref.key,
            'nomor_kamar': nomor_kamar,
            'tipe_kamar_id': tipe_kamar_id,
            'status': status
        })

        flash('Kamar berhasil ditambahkan!', 'success')
        return redirect(url_for('kamar.index'))

    return render_template('kamar/form.html', action='Tambah', tipe_list=tipe_list)

@kamar_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tipe_list = get_clean_data('tipe_kamar')
    kamar = firebase_db.reference(f'kamar/{id}').get()

    if request.method == 'POST':
        firebase_db.reference(f'kamar/{id}').update({
            'nomor_kamar': request.form.get('nomor_kamar'),
            'tipe_kamar_id': request.form.get('tipe_kamar_id'),
            'status': request.form.get('status')
        })
        flash('Data kamar berhasil diubah!', 'success')
        return redirect(url_for('kamar.index'))

    return render_template('kamar/form.html', action='Edit', kamar=kamar, tipe_list=tipe_list)

@kamar_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    firebase_db.reference(f'kamar/{id}').delete()
    flash('Kamar berhasil dihapus!', 'warning')
    return redirect(url_for('kamar.index'))