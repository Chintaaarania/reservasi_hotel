from datetime import datetime
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
        
        # Konversi aman jumlah_bayar ke float agar template tidak error 500
        raw_jumlah = p.get('jumlah_bayar', 0)
        try:
            p['jumlah_bayar'] = float(raw_jumlah)
        except (ValueError, TypeError):
            p['jumlah_bayar'] = 0.0

        pembayaran_list.append(p)

    # Ambil reservasi yang belum lunas (pending)
    lunas_res_ids = {str(p.get('reservasi_id')) for p in pembayaran_raw if str(p.get('status_pembayaran', '')).lower() == 'lunas'}
    reservasi_pending = []
    for r_id, r in reservasi_raw.items():
        if r_id not in lunas_res_ids:
            tamu_info = tamu_raw.get(str(r.get('tamu_id')), {})
            r['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
            r['kode_reservasi'] = r.get('kode_reservasi', r_id)
            
            # Konversi total_harga ke float
            raw_total = r.get('total_harga', 0)
            try:
                r['total_harga'] = float(raw_total)
            except (ValueError, TypeError):
                r['total_harga'] = 0.0

            reservasi_pending.append(r)

    pembayaran_list.sort(key=lambda x: str(x.get('id', '')), reverse=True)
    return render_template('pembayaran/index.html', pembayaran_list=pembayaran_list, reservasi_pending=reservasi_pending)

@pembayaran_bp.route('/bayar', methods=['POST'])
def bayar():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reservasi_id = request.form.get('reservasi_id')
    metode = request.form.get('metode_pembayaran')
    raw_jumlah = request.form.get('jumlah_bayar')
    status = request.form.get('status_pembayaran', 'lunas')

    try:
        jumlah_bayar = float(raw_jumlah) if raw_jumlah else 0.0
    except (ValueError, TypeError):
        jumlah_bayar = 0.0

    try:
        ref = firebase_db.reference('pembayaran')
        new_ref = ref.push()
        new_ref.set({
            'id': new_ref.key,
            'reservasi_id': reservasi_id,
            'metode_pembayaran': metode,
            'jumlah_bayar': jumlah_bayar,
            'status_pembayaran': status,
            'tanggal_bayar': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        flash('Proses pembayaran berhasil disimpan!', 'success')
    except Exception as e:
        flash(f'Gagal menyimpan pembayaran: {e}', 'danger')

    return redirect(url_for('pembayaran.index'))

@pembayaran_bp.route('/kwitansi/<id>')
def kwitansi(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Cari data pembayaran spesifik
    ref = firebase_db.reference('pembayaran')
    all_pembayaran = ref.get()
    
    pembayaran = None
    if isinstance(all_pembayaran, dict):
        if id in all_pembayaran:
            pembayaran = all_pembayaran[id]
        else:
            for k, v in all_pembayaran.items():
                if isinstance(v, dict) and str(v.get('id')) == str(id):
                    pembayaran = v
                    break
    elif isinstance(all_pembayaran, list):
        for idx, item in enumerate(all_pembayaran):
            if isinstance(item, dict) and str(item.get('id', idx)) == str(id):
                pembayaran = item
                break

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

        raw_jumlah = pembayaran.get('jumlah_bayar', 0)
        try:
            pembayaran['jumlah_bayar'] = float(raw_jumlah)
        except (ValueError, TypeError):
            pembayaran['jumlah_bayar'] = 0.0

    return render_template('pembayaran/kwitansi.html', pembayaran=pembayaran)