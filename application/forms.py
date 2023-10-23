from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email, exists_username

class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Email(), Length(max=128)])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    fullname = StringField("full name", validators=[DataRequired(), Length(min=4, max=16)])
    email = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    password = PasswordField("password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("confirm_password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit = SubmitField("Sign up")

class EditProfile(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    email = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    profile_pic = FileField("profile picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("update profile")

class CreatePost(FlaskForm):
    caption = TextAreaField("caption")
    image = FileField("picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Create Post')

class EditPost(FlaskForm):
    caption = StringField("caption")
    # image = FileField('Edit Image', validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Save Changes')

class ResetPasswordForm(FlaskForm):
    old_pass = PasswordField("old password", validators=[DataRequired(), Length(min=8)])
    new_pass = PasswordField("new password", validators=[DataRequired(), Length(min=8)])
    confirm_pass = PasswordField("confirm new pass", validators=[DataRequired(), Length(min=8), EqualTo("new_pass")])
    submit = SubmitField("reset password")

class ForgotPasswordForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), not_exists_email])
    recaptcha = RecaptchaField()
    submit = SubmitField("send link verification to email")

# class VerificationResetPasswordForm(FlaskForm):
class Verification(FlaskForm):
    password = PasswordField("new password", validartors=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit = SubmitField("reset password")
