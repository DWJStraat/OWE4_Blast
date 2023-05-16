"""
Initiates the web app
Created on 12-apr-2023 by David
Collaborators: David, Douwe, Jalmar
Last modified on 12-apr-2023 by David
"""
import secrets
from flask import Flask, \
    request, \
    render_template, \
    make_response, \
    redirect, \
    url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, \
    login_user, \
    logout_user, \
    login_required, \
    current_user
from forms import *
from middle_tier import fastq_parser as fastq
from middle_tier.mariaDB_server_wrapper import server as mariaDB
import json

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

login_manager = LoginManager()

bootstrap = Bootstrap5(app)


# csrf = CSRFProtect(app)

# Cookies for storing login info and stuff

@app.route('/home/')
def home():
    """
    Home page, base page when website is visited.
    :return: rendered template home.html
    author: David, Jalmar
    """
    cookies = request.cookies
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    return render_template('home.html', title='Home')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login page, allows user to log in.
    If user is already logged in, redirects to log out page.
    :return: rendered template login.html
    author: David, Jalmar
    """
    cookies = request.cookies
    if 'username' in cookies and 'password' in cookies:
        log_out = Logout()
        if log_out.validate_on_submit():
            resp = make_response(render_template('logout.html',
                                                 form=log_out,
                                                 message='You are logged out. '
                                                         'Refresh '
                                                         'the page or press '
                                                         'the button to '
                                                         'log in again'))
            resp.delete_cookie('username')
            resp.delete_cookie('password')
            resp.delete_cookie('database')
            return resp
        return render_template('logout.html',
                               form=log_out,
                               title='Logout',
                               message='You are logged in. Press the '
                                       'button to log out')
    else:
        log_in = LoginForm()
        if log_in.validate_on_submit():
            username = log_in.username.data
            # username = str(hash(username))
            password = log_in.password.data
            # password = str(hash(password))
            database = log_in.database.data
            # database = str(hash(database))
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            resp.set_cookie('database', database)
            return resp
        return render_template('login.html', form=log_in, title='Login')


@app.route('/cookies/')
def cookie():
    """
    Cookie page.
    notifies that cookies are used.
    cookie clicker game available for play.
    :return: rendered template cookie.html
    author: David, Douwe, Jalmar
    """
    cookies = request.cookies
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    return render_template('cookie.html', title='Cookies')


@app.route('/terms_of_service/')
def terms_of_service():
    """
    Terms of service page.
    displays terms of service.
    :return: rendered template terms_of_service.html
    author: David, Douwe, Jalmar
    """
    return render_template('terms_of_service.html', title='Terms of service')


@app.route('/input/', methods=['GET', 'POST'])
def inpoof():
    """
    Input page.
    Allows user to upload a file.
    :return: rendered template upload.html
    author: David, Jalmar
    """
    cookies = request.cookies
    form = UploadForm()
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    username = cookies['username']
    password = cookies['password']
    database = cookies['database']
    config = json.load(open('config.json'))
    host = config['DB_IP']
    if form.validate_on_submit():
        file = form.file.data
        file.save('uploads/dataset.xlsx')
        excel = fastq.excel('uploads/dataset.xlsx')
        excel.parse_for_db(use_json=False)
        values = excel.values
        server = mariaDB(host, username, password, database)
        server.mass_insert(values,
                           'DNA_seq',
                           ["ID", "seq_header", "quality", "sequence"])
        return render_template('upload.html',
                               title='Input',
                               form=form,
                               file=file.filename)
    return render_template('upload.html', title='Input', form=form)


@app.route('/search/')
def search():
    """
    Search page.
    Allows user to browse the database.
    :return: rendered template search.html
    author: David, Jalmar
    """
    cookies = request.cookies
    form = Search()
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        return redirect(url_for('search_results'))
    return render_template('search.html', title='Search', form=form)


@app.route('/search_results/', methods=['GET', 'POST'])
def search_results():
    """
    Search results page.
    Displays results from search.
    :return: rendered template search_results.html
    author: David, Jalmar
    """
    results = ['aaa', 'bbb', 'ccc', 'dd', 'eee']
    return render_template('search_results.html',
                           title='Search results',
                           result_list=results)


@app.errorhandler(404)
def page_not_found(e):
    """
    404 page.
    Displays 404 error.
    :param e: /
    :return: rendered template 404.html
    author: David, Jalmar
    """
    return render_template('404.html', title='404'), 404


if __name__ == '__main__':
    """
    Runs the app.
    """
    app.run(debug=True)
