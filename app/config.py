import os

QUESTIONS_PER_PAGE = 5
CSRF_ENABLED = True
SECRET_KEY = 'asdsdadasd21d1d2dsfd'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')