from flask import Blueprint, render_template, request, session, redirect, url_for
from firebase_admin import db as firebase_db

laporan_bp = Blueprint('laporan', __name__)

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

@laporan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    pembayaran_raw = get_clean_data('pembayaran')
    reservasi_raw = {str(r.get('id')): r for r in get_clean_data('reservasi')}
    tamu_raw = {str(t.get('id')): t for t in get_clean_data('tamu')}

    laporan = []
    total = 0.0

    for p in pembayaran_raw:
        # Hanya hitung pembayaran yang lunas
        if str(p.get('status_pembayaran', '')).lower() == 'lunas':
            tgl = str(p.get('tanggal_bayar', p.get('created_at', ''))).split(' ')[0]
            
            # Filter rentang tanggal jika diisi di formulir
            if start_date and tgl < start_date:
                continue
            if end_date and tgl > end_date:
                continue

            # Lengkapi info relasi reservasi & tamu
            res_info = reservasi_raw.get(str(p.get('reservasi_id')), {})
            tamu_info = tamu_raw.get(str(res_info.get('tamu_id')), {})

            p['kode_reservasi'] = res_info.get('kode_reservasi', res_info.get('id', '-'))
            p['nama_tamu'] = tamu_info.get('nama_lengkap', '-')
            
            # Konversi aman jumlah_bayar ke float
            raw_jumlah = p.get('jumlah_bayar', 0)
            try:
                jumlah_float = float(raw_jumlah)
            except (ValueError, TypeError):
                jumlah_float = 0.0

            p['jumlah_bayar'] = jumlah_float
            laporan.append(p)
            total += jumlah_float

    laporan.sort(key=lambda x: str(x.get('tanggal_bayar', '')), reverse=True)

    return render_template('laporan/index.html', laporan=laporan, total=total, start_date=start_date, end_date=end_date)