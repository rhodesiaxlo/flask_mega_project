from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Email, EqualTo,Length
from app_package.models import User,Post

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = StringField("password", validators=[DataRequired()])
    password2 = StringField("repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
    # captcha

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("please use a diffierent username")

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("please use a diffierent email")

class EditprofileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    aboutme = TextAreaField("aboutme", validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

