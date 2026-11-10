from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

checkin_checkout_bp = Blueprint('checkin_checkout', __name__)

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

@checkin_checkout_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_raw = get_clean_data('reservasi')
    tamu_raw = {str(t.get('id')): t for t in get_clean_data('tamu')}
    kamar_raw = {str(k.get('id')): k for k in get_clean_data('kamar')}

    reservasi_list = []
    for r in reservasi_raw:
        status_res = str(r.get('status_reservasi', '')).lower()
        if status_res in ['booking', 'checkin']:
            tamu_info = tamu_raw.get(str(r.get('tamu_id')), {})
            kamar_info = kamar_raw.get(str(r.get('kamar_id')), {})
            r['nama_tamu'] = tamu_info.get('nama_lengkap', 'Tamu Tidak Ditemukan')
            r['nomor_kamar'] = kamar_info.get('nomor_kamar', '-')
            reservasi_list.append(r)

    reservasi_list.sort(key=lambda x: str(x.get('tanggal_checkin', '')))

    return render_template('checkin_checkout/index.html', reservasi_list=reservasi_list)

@checkin_checkout_bp.route('/checkin/<id>', methods=['POST'])
def checkin(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        firebase_db.reference(f'reservasi/{id}').update({'status_reservasi': 'checkin'})
        res_data = firebase_db.reference(f'reservasi/{id}').get()
        if res_data and res_data.get('kamar_id'):
            firebase_db.reference(f"kamar/{res_data.get('kamar_id')}").update({'status': 'terisi'})

        flash('Proses Check-In berhasil!', 'success')
    except Exception as e:
        flash(f'Gagal Check-In: {e}', 'danger')

    return redirect(url_for('checkin_checkout.index'))

@checkin_checkout_bp.route('/checkout/<id>', methods=['POST'])
def checkout(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        firebase_db.reference(f'reservasi/{id}').update({'status_reservasi': 'checkout'})
        res_data = firebase_db.reference(f'reservasi/{id}').get()
        if res_data and res_data.get('kamar_id'):
            firebase_db.reference(f"kamar/{res_data.get('kamar_id')}").update({'status': 'kotor'})

        flash('Proses Check-Out berhasil! Status kamar menjadi kotor.', 'info')
    except Exception as e:
        flash(f'Gagal Check-Out: {e}', 'danger')

    return redirect(url_for('checkin_checkout.index'))