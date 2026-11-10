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

    layanan_raw = get_clean_layanan()
    layanan_list = []

    for l in layanan_raw:
        # Konversi harga ke float secara aman agar Jinja template tidak crash
        raw_harga = l.get('harga', 0)
        try:
            l['harga'] = float(raw_harga)
        except (ValueError, TypeError):
            l['harga'] = 0.0

        layanan_list.append(l)

    layanan_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
    return render_template('layanan/index.html', layanan_list=layanan_list)

@layanan_bp.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    nama_layanan = request.form.get('nama_layanan')
    raw_harga = request.form.get('harga')

    try:
        harga = float(raw_harga) if raw_harga else 0.0
    except (ValueError, TypeError):
        harga = 0.0

    ref = firebase_db.reference('layanan')
    new_ref = ref.push()
    new_ref.set({
        'id': new_ref.key,
        'nama_layanan': nama_layanan,
        'harga': harga
    })

    flash('Layanan tambahan berhasil ditambahkan!', 'success')
    return redirect(url_for('layanan.index'))

@layanan_bp.route('/hapus/<id>', methods=['POST'])
def hapus(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Cari dan hapus node spesifik
    ref = firebase_db.reference('layanan')
    all_layanan = ref.get()
    target_key = id

    if isinstance(all_layanan, dict):
        if id not in all_layanan:
            for k, v in all_layanan.items():
                if isinstance(v, dict) and str(v.get('id')) == str(id):
                    target_key = k
                    break
    elif isinstance(all_layanan, list):
        for idx, item in enumerate(all_layanan):
            if isinstance(item, dict) and str(item.get('id', idx)) == str(id):
                target_key = str(idx)
                break

    firebase_db.reference(f'layanan/{target_key}').delete()
    flash('Layanan berhasil dihapus!', 'warning')
    return redirect(url_for('layanan.index'))