from app import db
import datetime


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password = db.Column('password', db.String(100))
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Question(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    body = db.Column('body', db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column('title', db.String(50))


class Answer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column('text', db.String(100))
    likes = db.Column('likes', db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Like(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
