from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Username",
                                                                       "class": "user"})
    password = StringField('', validators=[DataRequired()], render_kw={"type": "password", "placeholder": "Password",
                                                                       "class": "pass"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})