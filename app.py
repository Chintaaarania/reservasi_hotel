import json
import os
import firebase_admin
from firebase_admin import credentials, db as firebase_db
from flask import Flask, render_template
from config import Config
from database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Wajib set SECRET_KEY untuk Flask session/login
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'reservasi-hotel-secret-key-123')

    # 2. Inisialisasi Firebase Admin SDK secara aman untuk Vercel
    cred_json = os.environ.get('FIREBASE_CREDENTIALS')
    db_url = os.environ.get('FIREBASE_DATABASE_URL')

    if cred_json and not firebase_admin._apps:
        try:
            cred_dict = json.loads(cred_json, strict=False)
            # Memperbaiki karakter newline \n dari Environment Variable Vercel
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': db_url
            })
            print("Firebase Admin SDK successfully initialized!")
        except Exception as e:
            print(f"Firebase initialization error: {e}")

    # 3. Inisialisasi Database lokal/SQLAlchemy (jika masih dipakai)
    db.init_app(app)

    # Halaman utama / Landing Page
    @app.route('/')
    def landing():
        return render_template('landing.html')

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.tamu import tamu_bp
    from routes.kamar import kamar_bp
    from routes.tipe_kamar import tipe_kamar_bp
    from routes.fasilitas import fasilitas_bp
    from routes.reservasi import reservasi_bp
    from routes.checkin_checkout import checkin_checkout_bp
    from routes.layanan import layanan_bp
    from routes.pembayaran import pembayaran_bp
    from routes.laporan import laporan_bp
    from routes.pengaturan import pengaturan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tamu_bp, url_prefix='/tamu')
    app.register_blueprint(kamar_bp, url_prefix='/kamar')
    app.register_blueprint(tipe_kamar_bp, url_prefix='/tipe-kamar')
    app.register_blueprint(fasilitas_bp, url_prefix='/fasilitas')
    app.register_blueprint(reservasi_bp, url_prefix='/reservasi')
    app.register_blueprint(checkin_checkout_bp, url_prefix='/checkin-checkout')
    app.register_blueprint(layanan_bp, url_prefix='/layanan')
    app.register_blueprint(pembayaran_bp, url_prefix='/pembayaran')
    app.register_blueprint(laporan_bp, url_prefix='/laporan')
    app.register_blueprint(pengaturan_bp, url_prefix='/pengaturan')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)