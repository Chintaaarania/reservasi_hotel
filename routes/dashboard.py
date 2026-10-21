from flask import Blueprint, render_template, session, redirect, url_for
from database import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    total_kamar = db.session.execute(db.text("SELECT COUNT(*) FROM kamar")).scalar() or 0
    kamar_terisi = db.session.execute(db.text("SELECT COUNT(*) FROM kamar WHERE status = 'terisi'")).scalar() or 0
    reservasi_aktif = db.session.execute(db.text("SELECT COUNT(*) FROM reservasi WHERE status_reservasi IN ('booking', 'checkin')")).scalar() or 0
    total_tamu = db.session.execute(db.text("SELECT COUNT(*) FROM tamu")).scalar() or 0

    return render_template(
        'dashboard.html',
        total_kamar=total_kamar,
        kamar_terisi=kamar_terisi,
        reservasi_aktif=reservasi_aktif,
        total_tamu=total_tamu
    )