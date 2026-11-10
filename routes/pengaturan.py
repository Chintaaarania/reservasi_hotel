from flask import Blueprint, render_template, session, redirect, url_for
from firebase_admin import db as firebase_db

pengaturan_bp = Blueprint('pengaturan', __name__)

def get_clean_logs():
    raw_data = firebase_db.reference('activity_log').get()
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

@pengaturan_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template('pengaturan/index.html')

@pengaturan_bp.route('/log')
def log():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    logs_raw = get_clean_logs()
    users_raw = {str(u.get('id')): u for u in get_clean_logs_users()}

    logs = []
    for l in logs_raw:
        u_info = users_raw.get(str(l.get('user_id')), {})
        l['username'] = u_info.get('username', l.get('username', 'System'))
        logs.append(l)

    logs.sort(key=lambda x: str(x.get('created_at', '')), reverse=True)
    return render_template('pengaturan/log.html', logs=logs)

def get_clean_logs_users():
    raw_data = firebase_db.reference('users').get()
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