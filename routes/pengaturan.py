from flask import Blueprint, render_template, session, redirect, url_for
from database import db

# Pastikan nama variabel di bawah ini adalah pengaturan_bp
pengaturan_bp = Blueprint('pengaturan', __name__)

@pengaturan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template('pengaturan/index.html')

@pengaturan_bp.route('/log')
def log():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard.index'))

    logs = db.session.execute(db.text("""
        SELECT al.*, u.username 
        FROM activity_log al
        JOIN users u ON al.user_id = u.id
        ORDER BY al.timestamp DESC
    """)).fetchall()

    return render_template('pengaturan/log.html', logs=logs)