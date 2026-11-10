from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from firebase_admin import db as firebase_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Ambil node data 'users' dari Firebase Realtime Database
        ref = firebase_db.reference('users')
        users_data = ref.get()

        user = None
        user_id = None

        # 2. Cari user berdasarkan field 'username' di Firebase
        if users_data and isinstance(users_data, dict):
            for uid, user_info in users_data.items():
                if isinstance(user_info, dict) and user_info.get('username') == username:
                    user = user_info
                    user_id = uid
                    break

        # 3. Verifikasi password (support password hash maupun plain text jika belum di-hash)
        if user:
            password_valid = False
            password_in_db = user.get('password_hash') or user.get('password')

            if password_in_db:
                if password_in_db.startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
                    password_valid = check_password_hash(password_in_db, password)
                else:
                    password_valid = (password_in_db == password)

            if password_valid:
                session['user_id'] = user_id
                session['username'] = user.get('username')
                session['role'] = user.get('role', 'admin')
                session['nama_lengkap'] = user.get('nama_lengkap', user.get('username'))
                flash('Login berhasil!', 'success')
                return redirect(url_for('dashboard.index'))

        flash('Username atau password salah.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar dari sistem.', 'info')
    return redirect(url_for('auth.login'))