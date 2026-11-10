from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

reservasi_bp = Blueprint('reservasi', __name__)

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

@reservasi_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_raw = get_clean_data('reservasi')
    tamu_raw = {str(t.get('id')): t for t in get_clean_data('tamu')}
    kamar_raw = {str(k.get('id')): k for k in get_clean_data('kamar')}

    reservasi_list = []
    for r in reservasi_raw:
        tamu_info = tamu_raw.get(str(r.get('tamu_id')), {})
        kamar_info = kamar_raw.get(str(r.get('kamar_id')), {})
        
        r['nama_tamu'] = tamu_info.get('nama_lengkap', 'Tamu Tidak Ditemukan')
        r['nomor_kamar'] = kamar_info.get('nomor_kamar', '-')
        reservasi_list.append(r)

    reservasi_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
    return render_template('reservasi/index.html', reservasi_list=reservasi_list)


@reservasi_bp.route('/buat', methods=['GET', 'POST'])
def buat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        tamu_id = request.form.get('tamu_id')
        kamar_id = request.form.get('kamar_id')
        checkin_str = request.form.get('tanggal_checkin')
        checkout_str = request.form.get('tanggal_checkout')
        user_id = session.get('user_id')

        try:
            # 1. Hitung total malam dan total harga
            d1 = datetime.strptime(checkin_str, '%Y-%m-%d')
            d2 = datetime.strptime(checkout_str, '%Y-%m-%d')
            total_malam = max((d2 - d1).days, 1)

            # Ambil data kamar & tipe kamar dari Firebase untuk dapat harga
            kamar_data = firebase_db.reference(f'kamar/{kamar_id}').get() or {}
            tipe_id = kamar_data.get('tipe_kamar_id')
            tipe_data = firebase_db.reference(f'tipe_kamar/{tipe_id}').get() or {}
            
            raw_harga = tipe_data.get('harga_per_malam', 0)
            try:
                harga_per_malam = float(raw_harga)
            except (ValueError, TypeError):
                harga_per_malam = 0.0

            total_harga = total_malam * harga_per_malam
            kode_res = f"REV-{int(datetime.now().timestamp())}"

            # 2. Simpan reservasi baru ke Firebase
            ref = firebase_db.reference('reservasi')
            new_ref = ref.push()
            new_reservasi = {
                'id': new_ref.key,
                'kode_reservasi': kode_res,
                'tamu_id': tamu_id,
                'kamar_id': kamar_id,
                'tanggal_checkin': checkin_str,
                'tanggal_checkout': checkout_str,
                'total_malam': total_malam,
                'total_harga': total_harga,
                'user_id': user_id,
                'status_reservasi': 'booking',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            new_ref.set(new_reservasi)

            # 3. Update status kamar menjadi 'terisi'
            firebase_db.reference(f'kamar/{kamar_id}').update({'status': 'terisi'})

            flash('Reservasi berhasil dibuat!', 'success')
            return redirect(url_for('reservasi.index'))
        except Exception as e:
            flash(f'Gagal membuat reservasi: {e}', 'danger')

    # Data untuk Form (GET)
    tamu_list = get_clean_data('tamu')
    kamar_raw = get_clean_data('kamar')
    tipe_kamar_raw = {str(tk.get('id')): tk for tk in get_clean_data('tipe_kamar')}

    kamar_list = []
    for k in kamar_raw:
        if str(k.get('status', '')).lower() == 'tersedia':
            tk_info = tipe_kamar_raw.get(str(k.get('tipe_kamar_id')), {})
            k['nama_tipe'] = tk_info.get('nama_tipe', '-')
            
            # Konversi aman ke float agar template HTML tidak crash saat formatting
            raw_harga = tk_info.get('harga_per_malam', 0)
            try:
                k['harga_per_malam'] = float(raw_harga)
            except (ValueError, TypeError):
                k['harga_per_malam'] = 0.0

            kamar_list.append(k)

    return render_template('reservasi/create.html', tamu_list=tamu_list, kamar_list=kamar_list)


@reservasi_bp.route('/detail/<id>')
def detail(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    res_data = firebase_db.reference(f'reservasi/{id}').get()
    
    if not res_data:
        all_reservasi = get_clean_data('reservasi')
        res_data = next((r for r in all_reservasi if str(r.get('id')) == str(id)), None)

    if res_data:
        tamu_info = firebase_db.reference(f"tamu/{res_data.get('tamu_id')}").get() or {}
        kamar_info = firebase_db.reference(f"kamar/{res_data.get('kamar_id')}").get() or {}
        tipe_info = firebase_db.reference(f"tipe_kamar/{kamar_info.get('tipe_kamar_id')}").get() or {}

        res_data['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
        res_data['nomor_telepon'] = tamu_info.get('nomor_telepon', '-')
        res_data['nomor_kamar'] = kamar_info.get('nomor_kamar', '-')
        res_data['nama_tipe'] = tipe_info.get('nama_tipe', '-')

    return render_template('reservasi/detail.html', reservasi=res_data)