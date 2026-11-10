from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from firebase_admin import db as firebase_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        ref = firebase_db.reference('users')
        users_data = ref.get()

        user = None
        user_id = None

        if users_data:
            # 1. Jika data dari Firebase dibaca sebagai List/Array (seperti di Firebase Console)
            if isinstance(users_data, list):
                for idx, user_info in enumerate(users_data):
                    if isinstance(user_info, dict):
                        if str(user_info.get('username', '')).strip().lower() == str(username).strip().lower():
                            user = user_info
                            user_id = user_info.get('id', idx)
                            break

            # 2. Jika data dari Firebase dibaca sebagai Dictionary
            elif isinstance(users_data, dict):
                for uid, user_info in users_data.items():
                    if isinstance(user_info, dict):
                        if str(user_info.get('username', '')).strip().lower() == str(username).strip().lower():
                            user = user_info
                            user_id = user_info.get('id', uid)
                            break

        # Verifikasi User dan Password Hash
        if user:
            password_in_db = str(user.get('password_hash') or user.get('password', ''))
            password_valid = False

            # Cek hash scrypt / pbkdf2 dari Werkzeug
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