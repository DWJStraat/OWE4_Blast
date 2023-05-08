# Initiates the web app
# Created on 12-apr-2023 by David
# Collaborators: David, Douwe, Jalmar
# Last modified on 12-apr-2023 by David
import secrets
from flask import Flask, request, render_template, make_response
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import *

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

login_manager = LoginManager()

bootstrap = Bootstrap5(app)


# csrf = CSRFProtect(app)

# Cookies for storing login info and stuff

@app.route('/', methods=['GET', 'POST'])
def login():
    log_in = LoginForm()
    if log_in.validate_on_submit():
        username = log_in.username.data
        username = str(hash(username))
        password = log_in.password.data
        password = str(hash(password))
        resp = make_response(render_template('login.html', log_in=log_in))
        resp.set_cookie('username', username)
        resp.set_cookie('password', password)
        return resp
    return render_template('login.html', log_in=log_in)


if __name__ == '__main__':
    app.run(debug=True)
