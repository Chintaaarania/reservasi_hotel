from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import db as firebase_db

pembayaran_bp = Blueprint('pembayaran', __name__)

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

@pembayaran_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    pembayaran_raw = get_clean_data('pembayaran')
    reservasi_raw = {str(r.get('id')): r for r in get_clean_data('reservasi')}
    tamu_raw = {str(t.get('id')): t for t in get_clean_data('tamu')}

    pembayaran_list = []
    for p in pembayaran_raw:
        res_info = reservasi_raw.get(str(p.get('reservasi_id')), {})
        tamu_info = tamu_raw.get(str(res_info.get('tamu_id')), {})
        p['kode_reservasi'] = res_info.get('kode_reservasi', res_info.get('id', '-'))
        p['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
        pembayaran_list.append(p)

    # Reservasi pending (belum lunas)
    lunas_res_ids = {str(p.get('reservasi_id')) for p in pembayaran_raw if str(p.get('status_pembayaran')).lower() == 'lunas'}
    reservasi_pending = []
    for r_id, r in reservasi_raw.items():
        if r_id not in lunas_res_ids:
            tamu_info = tamu_raw.get(str(r.get('tamu_id')), {})
            r['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
            r['kode_reservasi'] = r.get('kode_reservasi', r_id)
            reservasi_pending.append(r)

    return render_template('pembayaran/index.html', pembayaran_list=pembayaran_list, reservasi_pending=reservasi_pending)

@pembayaran_bp.route('/bayar', methods=['POST'])
def bayar():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_id = request.form.get('reservasi_id')
    metode = request.form.get('metode_pembayaran')
    jumlah = request.form.get('jumlah_bayar')
    status = request.form.get('status_pembayaran')

    try:
        ref = firebase_db.reference('pembayaran')
        new_ref = ref.push()
        new_ref.set({
            'id': new_ref.key,
            'reservasi_id': reservasi_id,
            'metode_pembayaran': metode,
            'jumlah_bayar': jumlah,
            'status_pembayaran': status
        })
        flash('Proses pembayaran berhasil disimpan!', 'success')
    except Exception as e:
        flash(f'Gagal menyimpan pembayaran: {e}', 'danger')

    return redirect(url_for('pembayaran.index'))

@pembayaran_bp.route('/kwitansi/<id>')
def kwitansi(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    pembayaran = firebase_db.reference(f'pembayaran/{id}').get() or {}
    if pembayaran:
        res_info = firebase_db.reference(f"reservasi/{pembayaran.get('reservasi_id')}").get() or {}
        tamu_info = firebase_db.reference(f"tamu/{res_info.get('tamu_id')}").get() or {}
        kamar_info = firebase_db.reference(f"kamar/{res_info.get('kamar_id')}").get() or {}

        pembayaran['kode_reservasi'] = res_info.get('kode_reservasi', res_info.get('id', '-'))
        pembayaran['total_malam'] = res_info.get('total_malam', 1)
        pembayaran['tanggal_checkin'] = res_info.get('tanggal_checkin', '-')
        pembayaran['tanggal_checkout'] = res_info.get('tanggal_checkout', '-')
        pembayaran['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
        pembayaran['nomor_kamar'] = kamar_info.get('nomor_kamar', '-')

    return render_template('pembayaran/kwitansi.html', pembayaran=pembayaran)