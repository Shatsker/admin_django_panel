from pathlib import Path

import os

from dotenv import load_dotenv

from split_settings.tools import include


load_dotenv()

include(
    'components/database.py',
    'components/application_definition.py',
    'components/password_validation.py',
    'components/internationalization.py',
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ('127.0.0.1', 'localhost')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = (
    "127.0.0.1",
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
