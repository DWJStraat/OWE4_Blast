"""
Initiates the web app
Created on 12-apr-2023 by David
Collaborators: David, Douwe, Jalmar
Last modified on 12-apr-2023 by David
"""

import contextlib
import os
import secrets
from flask import Flask, \
    request, \
    render_template, \
    make_response, \
    redirect, \
    url_for, \
    session
from flask_bootstrap import Bootstrap5
from forms import *
from middle_tier import fastq_parser as fastq
from middle_tier.mariaDB_server_wrapper import Server as MariaDb
import json
from os.path import exists

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

bootstrap = Bootstrap5(app)
config = json.load(open('config.json', 'r'))


# csrf = CSRFProtect(app)

# Cookies for storing login info and stuff

@app.route('/')
def index():
    """
    Index page, redirects to home page.
    :return: redirect to home page
    """
    return render_template('index.html')


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
    log_in = LoginForm()
    if 'username' in cookies and 'password' in cookies:
        log_out = Logout()
        if log_out.validate_on_submit():
            resp = make_response(render_template('login.html',
                                                 form=log_in,
                                                 title='Login',
                                                 message=''))
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
        if log_in.validate_on_submit():
            username = log_in.username.data
            # username = str(hash(username))
            password = log_in.password.data
            # password = str(hash(password))
            database = log_in.database.data
            # database = str(hash(database))
            server = MariaDb(config['DB_IP'], username, password, database)
            connection = server.connect()
            with contextlib.suppress(Exception):
                server.disconnect()
            if connection is True:
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('username', username)
                resp.set_cookie('password', password)
                resp.set_cookie('database', database)
                return resp
            else:
                return render_template('login.html',
                                       form=log_in,
                                       title='Login',
                                       message='Incorrect username or '
                                               'password')
        return render_template('login.html', form=log_in, title='Login',
                               message='')


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
    Display terms of service.
    :return: rendered template terms_of_service.html
    author: David, Douwe, Jalmar
    """
    return render_template('terms_of_service.html', title='Terms of service')


@app.route('/input/', methods=['GET', 'POST'])
def input_page():
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
    host = config['DB_IP']
    if not exists('uploads'):
        os.mkdir('uploads')
    if not exists('uploads/dataset.xlsx'):
        with open('uploads/dataset.xlsx', 'w') as file:
            file.close()
    try:
        if form.validate_on_submit():
            file = form.file.data
            if not file.filename.endswith('.xlsx'):
                return render_template('upload.html',
                                       title='Input',
                                       form=form,
                                       file=file.filename,
                                       message='Incorrect file type.')
            file.save('uploads/dataset.xlsx')
            excel = fastq.Excel('uploads/dataset.xlsx')
            excel.parse_for_db(use_json=False)
            values = excel.values
            server = MariaDb(host, username, password, database)
            server.mass_insert(values,
                               'DNA_seq',
                               ["seq_header", "quality", "sequence"])
            return render_template('upload.html',
                                   title='Input',
                                   form=form,
                                   file=file.filename)
        return render_template('upload.html', title='Input', form=form)
    except Exception as e:
        return render_template('upload.html',
                               title='Input',
                               form=form,
                               message=f'Error: {e}')


@app.route('/search/', methods=['GET', 'POST'])
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
        session['organism'] = form.orgname.data
        session['protein'] = form.protname.data
        session['header'] = form.header.data
        session['sequence'] = form.seq.data
        return redirect(url_for('search_results'))
    return render_template('search.html', title='Search', form=form)


@app.route('/search_results/', methods=['GET', 'POST'])
def search_results():
    """
    Search results page.
    Display results from search.
    :return: rendered template search_results.html
    author: David, Jalmar
    """
    parameters = json.loads('{}')
    parameters['organism'] = session['organism']
    parameters['protein'] = session['protein']
    parameters['header'] = session['header']
    parameters['sequence'] = session['sequence']

    cookies = request.cookies
    if 'username' not in cookies or 'password' not in cookies:
        return redirect(url_for('login'))
    username = cookies['username']
    password = cookies['password']
    database = cookies['database']
    parameter = ''
    if parameters['organism'] != '':
        parameter += f'Br0.organism LIKE "%{parameters["organism"]}%" '
    if parameters['protein'] != '':
        if parameter != '':
            parameter += 'AND '
        parameter += f'Br0.Prot_name LIKE "%{parameters["protein"]}%" '
    if parameters['header'] != '':
        if parameter != '':
            parameter += 'AND '
        parameter += f'Br0.seq_header LIKE "%{parameters["header"]}%" '
    if parameters['sequence'] != '':
        if parameter != '':
            parameter += 'AND '
        parameter += f'Br0.sequence LIKE "%{parameters["sequence"]}%" '
    host = config['DB_IP']
    server = MariaDb(host, username, password, database)
    results = server.search('*', parameter)
    result_list = json.loads('{}')
    print(results)
    for result in results:
        result_list[result[11]] = {
            'id': result[0],
            'e_value': result[1],
            'identity_percentage': result[2],
            'query_cover': result[3],
            'accession_length': result[4],
            'max_score': result[5],
            'total_score': result[6],
            'accession': result[7],
            'organism': f'{result[8]}',
            'protein': result[9],
            'header': result[10],
            'sequence': result[11],
        }
        print(result_list)
    return render_template('search_results.html',
                           title='Search results',
                           results=result_list)


@app.errorhandler(404)
def page_not_found(e):
    """
    404 page.
    Displays 404 error.
    :param e: /
    :return: rendered template 404.html
    author: David, Jalmar
    """
    return render_template('404.html', title='404', error=e), 404


if __name__ == '__main__':
    """
    Runs the app.
    """
    app.run(debug=True)


def run():
    """
    Runs the app.
    """
    app.run()
