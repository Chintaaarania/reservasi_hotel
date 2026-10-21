from flask import Blueprint, render_template, request, session, redirect, url_for
from services.laporan_service import dapatkan_laporan_pendapatan

laporan_bp = Blueprint('laporan', __name__)

@laporan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    laporan, total = dapatkan_laporan_pendapatan(start_date, end_date)

    return render_template('laporan/index.html', laporan=laporan, total=total, start_date=start_date, end_date=end_date)