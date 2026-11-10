import os
from dotenv import load_dotenv

load_dotenv()

_raw_uri = os.getenv('DATABASE_URL')
_db_user = os.getenv('DB_USER', 'root')
_db_pass = os.getenv('DB_PASSWORD', '')
_db_host = os.getenv('DB_HOST', 'localhost')
_db_port = os.getenv('DB_PORT', '3306')
_db_name = os.getenv('DB_NAME', 'db_reservasi_hotel')

if _raw_uri:
    if _raw_uri.startswith('mysql://'):
        _raw_uri = _raw_uri.replace('mysql://', 'mysql+pymysql://', 1)
    _db_uri = _raw_uri
else:
    _db_uri = f"mysql+pymysql://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"

_force_ssl = os.getenv('DB_SSL', 'false').lower() in ('true', '1', 'yes')
_is_cloud = any(h in (_db_host + (_raw_uri or '')) for h in ['tidbcloud.com', 'aivencloud.com', 'clever-cloud.com'])

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-hotel')
    SQLALCHEMY_DATABASE_URI = _db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if _force_ssl or _is_cloud:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'ssl': {'check_hostname': False}
            }
        }
