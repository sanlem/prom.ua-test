from flask import render_template, Flask, request, flash, redirect, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
import forms
from models import User, Question, Answer, Like
from app import app, db, login_manager, bcrypt
from config import QUESTIONS_PER_PAGE


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    questions = Question.query.order_by(Question.id.desc())[:5]
    return render_template("index.html", questions=questions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password = bcrypt.generate_password_hash(form.password.data)
        # user = User(username=form.username.data, password=form.password.data)
        user = User(username=form.username.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/all')
def all():
    return render_template("index.html")


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = forms.LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        # user = User.query.filter_by(username=username, password=password).first()
        user = User.query.filter_by(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Wrong password or username.')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/questions')
@app.route('/questions/<int:page>')
def questions(page=1):
    questions = Question.query.order_by(Question.id.desc()).paginate(page, QUESTIONS_PER_PAGE, False)
    if page not in questions.iter_pages():
        # calculating the last page number
        num = len(Question.query.all())
        last_page = num // QUESTIONS_PER_PAGE + num % QUESTIONS_PER_PAGE
        flash("Such page doesn't exists. Redirected.")
        return redirect(url_for('questions', page=last_page))
    return render_template('questions.html', questions=questions)


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = forms.AskForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        question = Question(title=title, body=body, user_id=g.user.get_id())
        db.session.add(question)
        db.session.commit()
        flash('Question added.')
        return redirect(url_for('questions'))
    return render_template('ask.html', form=form)


@app.route('/question/<id>')
@app.route('/question/<id>/<int:page>')
def some_question(id, page=1):
    question = Question.query.filter_by(id=id).first_or_404()
    # answers = Answer.query.filter_by()
    # answers = Answer.query.filter_by(question_id=id).paginate(page, QUESTIONS_PER_PAGE, False)
    answers = question.answers.order_by(Answer.likes.desc()).paginate(page, QUESTIONS_PER_PAGE, False)
    if question.answers.all() and (page not in answers.iter_pages()):
        # calculating the last page number
        num = len(question.answers.all())
        last_page = num // QUESTIONS_PER_PAGE + num % QUESTIONS_PER_PAGE
        flash("Such page doesn't exists. Redirected.")
        return redirect(url_for('some_question', page=last_page, id=id))
    return render_template("some_question.html", question=question, answers=answers)


@app.route('/question/<id>/answer', methods=['GET', 'POST'])
@login_required
def answer(id):
    question = Question.query.get_or_404(id)
    form = forms.AnswerForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        answer = Answer(text=text, question_id=id, user_id=g.user.get_id())
        db.session.add(answer)
        db.session.commit()
        flash('Answer successfully added.')
        return redirect(url_for('some_question', id=id))
    return render_template('answer.html', form=form, question=question)


@app.route('/question/<id>/answer/<ans_id>/like')
@login_required
def vote(id, ans_id):
    answer = Answer.query.get_or_404(ans_id)
    if not Like.query.filter_by(question_id=id, author=g.user).first():
        like = Like(user_id=g.user.id, question_id=id, answer_id=ans_id)
        db.session.add(like)
        answer.likes = answer.likes + 1
        db.session.commit()
        flash('You have successfully voted.')
        return redirect(url_for('some_question', id=id))
    else:
        old_like = Like.query.filter_by(question_id=id, author=g.user).first()
        # decreasing old like
        previously_liked = Answer.query.filter_by(id=old_like.answer_id).first()
        previously_liked.likes = previously_liked.likes - 1
        db.session.delete(old_like)
        like = Like(user_id=g.user.id, question_id=id, answer_id=ans_id)
        db.session.add(like)
        answer.likes = answer.likes + 1
        db.session.commit()
        flash('You have revoted.')
        return redirect(url_for('some_question', id=id))


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(author=user).all()
    questions = Question.query.filter_by(author=user).all()
    return render_template('profile.html', user=user, answers_amount=len(answers), questions_amount=len(questions))


@app.route('/profile/<username>/answers')
@app.route('/profile/<username>/answers/<int:page>')
def users_answers(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    answers = user.answers.paginate(page, QUESTIONS_PER_PAGE, False)
    if user.answers.all() and (page not in answers.iter_pages()):
        # calculating the last page number
        num = len(user.answers.all())
        last_page = num // QUESTIONS_PER_PAGE + num % QUESTIONS_PER_PAGE
        flash("Such page doesn't exists. Redirected.")
        return redirect(url_for('users_answers', page=last_page, username=username))
    return render_template('users_answers.html', answers=answers, user=user)


@app.route('/profile/<username>/questions')
@app.route('/profile/<username>/questions/<int:page>')
def users_questions(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    questions = user.questions.paginate(page, QUESTIONS_PER_PAGE, False)
    if user.questions.all() and (page not in questions.iter_pages()):
        # calculating the last page number
        num = len(user.questions.all())
        last_page = num // QUESTIONS_PER_PAGE + num % QUESTIONS_PER_PAGE
        flash("Such page doesn't exists. Redirected.")
        return redirect(url_for('users_questions', page=last_page, username=username))
    return render_template('users_questions.html', questions=questions, user=user)
