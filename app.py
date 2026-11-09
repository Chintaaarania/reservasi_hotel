
from flask import Flask, render_template
from config import Config
from database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
