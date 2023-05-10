from flask_wtf import FlaskForm, CSRFProtect
from flask import Markup
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Username",
                                                                       "class": "user"})
    password = StringField('', validators=[DataRequired()], render_kw={"type": "password", "placeholder": "Password",
                                                                       "class": "pass"})
    terms = BooleanField(
        Markup('I agree to the <a onclick="location.href=\'/terms_of_service\'">Terms of Service</a>'),
        validators=[DataRequired()], render_kw={"class": "termsservice"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

class UploadForm(FlaskForm):
    file = FileField('', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})