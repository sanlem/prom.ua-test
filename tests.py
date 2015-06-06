#!bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Question, Answer, Like

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        user = User(username='sanlem', password='111111')
        db.session.add(user)
        db.session.commit()
        assert user.username == 'sanlem'
        assert user.password == '111111'
        assert user.id == int(user.get_id())

    def test_question_adding(self):
        user = User(username='sanlem', password='111111')
        db.session.add(user)
        db.session.commit()
        question1 = Question(title='Test title', body='123', user_id=user.id)
        db.session.add(question1)
        db.session.commit()
        assert question1.author == user
        assert question1.title == 'Test title'
        assert len(user.questions.all()) == 1
        question2 = Question(title='Test title', body='123', user_id=user.id)
        db.session.add(question2)
        db.session.commit()
        assert question2.author == user
        assert question2.title == 'Test title'
        assert len(user.questions.all()) == 2

    def test_question_answering(self):
        user = User(username='sanlem', password='111111')
        db.session.add(user)
        db.session.commit()
        question = Question(title='Test title', body='123', user_id=user.id)
        answer1 = Answer(text='test', question=question, author=user)
        db.session.add(question)
        db.session.add(answer1)
        db.session.commit()
        assert answer1.author == user
        assert answer1.text == 'test'
        assert len(user.answers.all()) == 1
        assert len(question.answers.all()) == 1
        answer2 = Answer(text='test', question_id=question.id, user_id=user.id)
        db.session.add(answer2)
        db.session.commit()
        assert answer1.text == answer2.text
        assert len(user.answers.all()) == 2
        assert len(question.answers.all()) == 2

    def test_likes(self):
    	user1 = User(username='sanlem', password='111111')
        user2 = User(username='sanlem1', password='111111')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        question = Question(title='Test title', body='123', user_id=user1.id)
        answer1 = Answer(text='test', question_id=question.id, user_id=user1.id)
        db.session.add(question)
        db.session.add(answer1)
        answer2 = Answer(text='test', question_id=question.id, user_id=user1.id)
        db.session.add(answer2)
        db.session.commit()
        assert answer1.likes == 0
        assert answer2.likes == answer1.likes
        like1 = Like(question_id=question.id, answer_id=answer1.id, user_id=user1.id)
        db.session.add(like1)
        db.session.commit()
        assert len(Like.query.filter_by(answer_id=answer1.id).all()) == 1
        like2 = Like(question_id=question.id, answer_id=answer1.id, user_id=user2.id)
        db.session.add(like2)
        db.session.commit()
        assert len(Like.query.filter_by(answer_id=answer1.id).all()) == 2
        assert len(Like.query.filter_by(answer_id=answer1.id).all()) != len(Like.query.filter_by(answer_id=answer2.id).all())


if __name__ == '__main__':
    unittest.main()
