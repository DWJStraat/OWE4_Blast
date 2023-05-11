# Initiates the web app
# Created on 12-apr-2023 by David
# Collaborators: David, Douwe, Jalmar
# Last modified on 12-apr-2023 by David
import secrets
from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import *
from time import time
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

login_manager = LoginManager()

bootstrap = Bootstrap5(app)


# csrf = CSRFProtect(app)

# Cookies for storing login info and stuff

@app.route('/home/')
def home():
    cookies = request.cookies
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    return render_template('home.html', title='Home')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cookies = request.cookies
    if 'username' in cookies and 'password' in cookies:
        log_out = Logout()
        if log_out.validate_on_submit():
            resp = make_response(render_template('logout.html', form=log_out, message='You are logged out. Refresh '
                                                                                      'the page or press the button to '
                                                                                      'log in again'))
            resp.delete_cookie('username')
            resp.delete_cookie('password')
            return resp
        return render_template('logout.html', form=log_out, title='Logout', message='You are logged in. Press the '
                                                                                    'button to log out')
    else:
        log_in = LoginForm()
        if log_in.validate_on_submit():
            username = log_in.username.data
            username = str(hash(username))
            password = log_in.password.data
            password = str(hash(password))
            resp = make_response(render_template('login.html', form=log_in))
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            return resp
        return render_template('login.html', form=log_in, title='Login')


@app.route('/cookies/')
def cookies():
    cookies = request.cookies
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    return render_template('cookie.html', title='Cookies')


@app.route('/terms_of_service/')
def terms_of_service():
    return render_template('terms_of_service.html', title='Terms of service')


@app.route('/input/', methods=['GET', 'POST'])
def input():
    cookies = request.cookies
    form = UploadForm()
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        file = form.file.data
        filename = f'{int(time())}-{secure_filename(file.filename)}'
        file.save(f'uploads/{filename}')
        return render_template('upload.html', title='Input', form=form, file=file.filename)
    return render_template('upload.html', title='Input', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404


if __name__ == '__main__':
    app.run(debug=True)
