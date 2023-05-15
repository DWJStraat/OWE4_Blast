from flask_wtf import FlaskForm, CSRFProtect
from flask import Markup
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Username",
                                                                       "class": "user"})
    password = StringField('', validators=[DataRequired()], render_kw={"type": "password", "placeholder": "Password",
                                                                       "class": "pass"})
    database = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Database"})
    terms = BooleanField(
        Markup('I agree to the <a onclick="location.href=\'/terms_of_service\'">Terms of Service</a>'),
        validators=[
            # DataRequired()
        ], render_kw={"class": "termsservice"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

class UploadForm(FlaskForm):
    file = FileField('', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

class Logout(FlaskForm):
    submit = SubmitField('Logout', render_kw={"class": "btn btn-primary"})

class Login(FlaskForm):
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"}, onclick="location.href=\'/login\'")