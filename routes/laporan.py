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
                items.append(value)
    elif isinstance(raw_data, list):
        for item in raw_data:
            if isinstance(item, dict):
                items.append(item)
    return items

@laporan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    pembayaran_raw = get_clean_data('pembayaran')
    laporan = []
    total = 0

    for p in pembayaran_raw:
        if str(p.get('status_pembayaran', '')).lower() == 'lunas':
            tgl = str(p.get('tanggal_bayar', p.get('created_at', '')))
            
            # Filter rentang tanggal jika diisi
            if start_date and tgl < start_date:
                continue
            if end_date and tgl > end_date:
                continue

            jumlah = float(p.get('jumlah_bayar', 0))
            laporan.append(p)
            total += jumlah

    return render_template('laporan/index.html', laporan=laporan, total=total, start_date=start_date, end_date=end_date)