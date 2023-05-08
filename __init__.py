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


if __name__ == '__main__':
    app.run(debug=True)
