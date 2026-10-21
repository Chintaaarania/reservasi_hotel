from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Bypass Total: Langsung set session dan izinkan masuk untuk username apapun
        session['user_id'] = 1
        session['username'] = username if username else 'admin'
        session['role'] = 'admin'
        session['nama_lengkap'] = 'Administrator'
        
        flash('Login berhasil!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar dari sistem.', 'info')
    return redirect(url_for('auth.login'))