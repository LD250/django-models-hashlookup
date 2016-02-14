SECRET_KEY = 'fake'
INSTALLED_APPS = [
    "tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

