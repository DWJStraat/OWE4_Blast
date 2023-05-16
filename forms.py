from flask_wtf import FlaskForm, CSRFProtect
from flask import Markup
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Username",
                                                                       "class": "user",
                                                                       "style": 'scale: 200%',
                                                                       'margin': '0 auto'})
    password = StringField('', validators=[DataRequired()], render_kw={"type": "password", "placeholder": "Password",
                                                                       "class": "pass",
                                                                       "style": 'scale: 200%'})
    database = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Database",
                                                                       "style": 'scale: 200%',
                                                                       'title': 'Enter the name of the database '
                                                                       }
                           )
    terms = BooleanField(
        Markup('I agree to the <a onclick="location.href=\'/terms_of_service\'">Terms of Service</a>'),
        validators=[
            # DataRequired()
        ], render_kw={"class": "termsservice"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class UploadForm(FlaskForm):
    file = FileField('', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                 "style": 'scale: 200%'})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class Logout(FlaskForm):
    submit = SubmitField('Logout', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class Login(FlaskForm):
    submit = SubmitField('Login',
                         render_kw={"class": "btn btn-primary",
                                    "style": 'scale: 200%'},
                         onclick="location.href=\'/login\'")


class Search(FlaskForm):
    orgname = StringField(Markup('<button_orgname class="info-button", onclick="infoPopUp()", title="info">'
                                 '<img src = "../static/image/info_FILL0_wght400_GRAD0_opsz48.png">'
                                 '<span class="popuptext" id="infopopup">test text</span>')
    , render_kw={"placeholder": "Name of organism"})
    protname = StringField('', render_kw={"placeholder": "Name of protein"})
    header = StringField('', render_kw={"placeholder": "Header of sequence"})
    seq = StringField('', render_kw={"placeholder": "Sequence"})
    eval_threshold = StringField('', render_kw={"placeholder": "E-value threshold"})
    query_coverage = StringField('', render_kw={"placeholder": "Query coverage"})
    origin = StringField('', render_kw={"placeholder": "Origin"})
    submit = SubmitField('Search', render_kw={"class": "btn btn-primary"})
