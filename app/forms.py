from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, max=25)
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=25)
    ])
    remember_me = BooleanField('remember_me', default = False)


class AskForm(Form):
    title = TextField('Title', [validators.Length(max=50), validators.Required()])
    body = TextAreaField('Body', [validators.Length(max=500)])


class AnswerForm(Form):
    text = TextAreaField('', [validators.Length(max=500), validators.Required()])
