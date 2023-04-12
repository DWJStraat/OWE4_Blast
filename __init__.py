# Initiates the web app
# Created on 12-apr-2023 by David
# Collaborators: David, Douwe, Jalmar
# Last modified on 12-apr-2023 by David
import secrets
from flask import Flask, CSRFProtect

from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']


bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


if __name__ == '__main__':
    app.run(debug=True)


