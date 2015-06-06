from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('likes', Integer),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('timestamp', DateTime),
)

question = Table('question', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String),
    Column('password', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].drop()
    pre_meta.tables['question'].drop()
    pre_meta.tables['user'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].create()
    pre_meta.tables['question'].create()
    pre_meta.tables['user'].create()
