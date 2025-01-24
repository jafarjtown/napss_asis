from .base import *
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# import dj_database_url
# production specific settings
# DEBUG = False
# other production settings...


DEBUG = False



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
MEDIA_ROOT = BASE_DIR.parent / 'media.abusitehub.com.ng/'
MEDIA_URL = 'http://media.abusitehub.com.ng/'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_error.txt'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}