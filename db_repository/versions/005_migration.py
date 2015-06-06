from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
question = Table('question', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=150)),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
    Column('title', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['question'].columns['text'].drop()
    post_meta.tables['question'].columns['body'].create()
    post_meta.tables['question'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['question'].columns['text'].create()
    post_meta.tables['question'].columns['body'].drop()
    post_meta.tables['question'].columns['title'].drop()
