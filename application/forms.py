from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email, exists_username

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    fullname = StringField("full name", validators=[DataRequired(), Length(min=4, max=16)])
    email = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    password = PasswordField("password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("confirm_password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit = SubmitField("Sign up")

class EditProfileForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12)])
    fullname = StringField("full name", validators=[DataRequired(), Length(min=4, max=16)])
    profile_pic = FileField("profile picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    bio = TextAreaField("bio")
    submit = SubmitField("update profile")

class CreatePostForm(FlaskForm):
    caption = TextAreaField("caption")
    post_pic = FileField("picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Create Post')

class EditPostForm(FlaskForm):
    caption = StringField("caption")
    photo = FileField("photo", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Save Changes')

class ResetPasswordForm(FlaskForm):
    old_pass = PasswordField("old password", validators=[DataRequired(), Length(min=4)])
    new_pass = PasswordField("new password", validators=[DataRequired(), Length(min=4)])
    confirm_pass = PasswordField("confirm new pass", validators=[DataRequired(), Length(min=4), EqualTo("new_pass")])
    submit = SubmitField("reset password")

class ForgotPasswordForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), not_exists_email])
    recaptcha = RecaptchaField()
    submit = SubmitField("send link verification to email")

class VerificationForm(FlaskForm):
    password = PasswordField("new password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit = SubmitField("reset password")

