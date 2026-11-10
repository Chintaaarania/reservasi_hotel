from flask import Blueprint, render_template, session, redirect, url_for, flash
from firebase_admin import db as firebase_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    # 1. Cek proteksi session login
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Helper function untuk mengubah data Firebase (dict/list) ke list item yang valid
    def get_clean_list(data):
        if not data:
            return []
        if isinstance(data, dict):
            return list(data.values())
        if isinstance(data, list):
            return [item for item in data if item is not None]
        return []

    try:
        # 2. Ambil data dari node Firebase
        data_kamar = get_clean_list(firebase_db.reference('kamar').get())
        data_reservasi = get_clean_list(firebase_db.reference('reservasi').get())
        data_tamu = get_clean_list(firebase_db.reference('tamu').get())

        # 3. Hitung statistik sesuai variabel template Anda
        total_kamar = len(data_kamar)
        
        # Hitung kamar dengan status 'terisi'
        kamar_terisi = sum(
            1 for k in data_kamar 
            if isinstance(k, dict) and str(k.get('status', '')).lower() == 'terisi'
        )

        # Hitung reservasi aktif ('booking' atau 'checkin')
        reservasi_aktif = sum(
            1 for r in data_reservasi 
            if isinstance(r, dict) and str(r.get('status_reservasi', '')).lower() in ['booking', 'checkin']
        )

        total_tamu = len(data_tamu)

    except Exception as e:
        print(f"Firebase fetch error on dashboard: {e}")
        total_kamar = 0
        kamar_terisi = 0
        reservasi_aktif = 0
        total_tamu = 0

    return render_template(
        'dashboard.html',
        total_kamar=total_kamar,
        kamar_terisi=kamar_terisi,
        reservasi_aktif=reservasi_aktif,
        total_tamu=total_tamu
    )