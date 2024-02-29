import os
from .constants import __version__


JWT_KEY = os.getenv('JWT_KEY')

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

FERNET_KEY = os.getenv('FERNET_KEY')

AWS_SECRET_ACCESS_KEY = os.getenv('C_AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.getenv('C_AWS_ACCESS_KEY_ID')
AWS_REGION_NAME = os.getenv('C_AWS_REGION_NAME')


S3_BUCKET = os.getenv('S3_BUCKET')

BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

VERSION: str = '1.0.0'