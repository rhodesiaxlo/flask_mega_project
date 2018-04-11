from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Email, EqualTo,Length
from app_package.models import User,Post
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    password = PasswordField(_l('password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('remember me'))
    submit = SubmitField(_l('Sign in'))

class RegisterForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired(), Email()])
    password = StringField(_l('password'), validators=[DataRequired()])
    password2 = StringField('repeat password', validators=[DataRequired(), EqualTo(_l('password'))])
    submit = SubmitField(_l('Register'))
    # captcha

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('please use a diffierent username'))

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_l('please use a diffierent email'))

class EditprofileForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    aboutme = TextAreaField(_l('aboutme'), validators=[Length(min=0,max=140)])
    submit = SubmitField(_l('Submit'))

class PostForm(FlaskForm):
    body = TextAreaField(_l('body'), validators=[DataRequired(),Length(min=0,max=140)])
    submit = SubmitField(_l('Submit'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(_l('Request Password Reset'))