"""
This file contains the forms used in the website. The forms are used to
collect data from the user. The forms are used to log in, log out, upload
a file and search the database. The forms are created using the FlaskForm
class from the flask_wtf module. The forms are rendered using the render_kw
parameter. The forms are submitted using the submit button. The forms are
validated using the validator's parameter. The forms are used in the
__init__.py file.

author: David, Douwe, Jalmar
"""

from flask_wtf import FlaskForm
from flask import Markup
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
    LoginForm is the setup for the login form. This form is used to log in
    to the website. It contains three fields: username, password and database.
    The username and password fields are used to log in to the database.
    The database field is used to select the database to be used.
    The form also contains a checkbox for the terms of service.
    The form is submitted with the submit button.

    :param FlaskForm: parent class
    :return: rendered template login.html
    author: David
    """
    username = StringField('', validators=[DataRequired()],
                           render_kw={"placeholder": "Username",
                                      "class": "user",
                                      "style": 'scale: 200%',
                                      'margin': '0 auto'})
    password = StringField('', validators=[DataRequired()],
                           render_kw={"type": "password",
                                      "placeholder": "Password",
                                      "class": "pass",
                                      "style": 'scale: 200%'})
    database = StringField('', validators=[DataRequired()],
                           render_kw={"placeholder": "Database",
                                      "style": 'scale: 200%',
                                      'title':
                                          'Enter the name of the database '})
    terms = BooleanField(
        Markup('I agree to the '
               '<a onclick="location.href=\'/terms_of_service\'">'
               'Terms of Service</a>'),
        validators=[
            # DataRequired()
        ], render_kw={"class": "termsservice"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class UploadForm(FlaskForm):
    """
    UploadForm is the setup for the upload form. This form is used to upload
    a file to the website. It contains one field: file. The file field is used
    to upload a file to the website. The form is submitted with the submit
    button.

    :param FlaskForm: parent class
    :return: rendered template upload.html
    author: David
    """
    file = FileField('', validators=[DataRequired()],
                     render_kw={"class": "form-control",
                                "style": 'scale: 200%'})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class Logout(FlaskForm):
    """
    LogoutForm is the setup for the logout form. This form is used to log out
    of the website. It contains one field: submit. The submit field is used
    to log out of the website. The form is submitted with the submit button.

    :param FlaskForm: parent class
    :return: rendered template logout.html
    author: David
    """
    submit = SubmitField('Logout', render_kw={"class": "btn btn-primary",
                                              "style": 'scale: 200%'})


class Login(FlaskForm):
    """
    Login is the setup for the login form. This form is used to log in to the
    website. It contains one field: submit. The submit field is used to log in
    to the website. The form is submitted with the submit button.

    :param FlaskForm: parent class
    :return: rendered template login.html
    author: David
    """
    submit = SubmitField('Login',
                         render_kw={"class": "btn btn-primary",
                                    "style": 'scale: 200%'},
                         onclick="location.href=\'/login\'")


class Search(FlaskForm):
    """
    Search is the setup for the search form. This form is used to search
    the database. It contains three fields: orgname, protname and header.
    The orgname field is used to search for the organism name in the database.
    The protname field is used to search for the protein name in the database.
    The header field is used to search for the header in the database.
    The form is submitted with the submit button.

    :param FlaskForm: parent class
    :return: rendered template search.html
    author: David, Douwe, Jalmar
    """
    orgname = StringField(Markup('<button_orgname class="info-button", '
                                 'onclick="infoPopUp_orgname()", title="info">'
                                 '<img src = "../static/image'
                                 '/info_FILL0_wght400_GRAD0_opsz48.png">'
                                 '<span class="popuptext_bottom" '
                                 'id="infopopup_orgname">'
                                 '<b1>Organism name</b1><br>'
                                 '<b2>description</b2><br>'
                                 '&emsp;Searches for these '
                                 '&emsp;words in the organism name list'
                                 '&emsp;in the database<br>'
                                 '<b2>Be aware of the following:</b2><br>'
                                 '<ul>'
                                 '<li>Searches are case sensitive</li>'
                                 '</ul>'
                                 '<b2>Syntax-equivalent '
                                 'in the normal search</b2><br>'
                                 'homo sapiens'
                                 '</span>'),
                          render_kw={"placeholder": "Name of organism"})
    protname = StringField(Markup('<button_protname class="info-button", '
                                  'onclick="infoPopUp_protname()", '
                                  'title="info">'
                                  '<img src = "../static/image'
                                  '/info_FILL0_wght400_GRAD0_opsz48.png">'
                                  '<span class="popuptext_bottom" '
                                  'id="infopopup_protname">'
                                  '<b1>Protein name</b1><br>'
                                  '<b2>description</b2><br>'
                                  '&emsp;Searches for these '
                                  '&emsp;words in the protein list '
                                  '&emsp;of the database<br>'
                                  '<b2>Be aware of the following:</b2><br>'
                                  '<ul>'
                                  '<li>Searches are case sensitive</li>'
                                  '</ul>'
                                  '<b2>Syntax-equivalent '
                                  'in the normal search</b2><br>'
                                  'insulin'
                                  '</span>'),
                           render_kw={"placeholder": "Name of protein"})
    header = StringField(Markup('<button_header class="info-button", '
                                'onclick="infoPopUp_header()", title="info">'
                                '<img src = "../static/image'
                                '/info_FILL0_wght400_GRAD0_opsz48.png">'
                                '<span class="popuptext_bottom" '
                                'id="infopopup_header">'
                                '<b1>header of the sequence</b1><br>'
                                '<b2>description</b2><br>'
                                '&emsp;Searches for this '
                                '&emsp; phrase in the blast result list '
                                '&emsp;of the database<br>'
                                '<b2>Be aware of the following:</b2><br>'
                                '<ul>'
                                '<li>Searches are case sensitive</li>'
                                '</ul>'
                                '<b2>Syntax-equivalent '
                                'in the normal search</b2><br>'
                                'NP_001035835.1'
                                '</span>'),
                         render_kw={"placeholder": "Header of sequence"})
    seq = StringField(Markup('<button_seq class="info-button", '
                             'onclick="infoPopUp_seq()", title="info">'
                             '<img src = "../static/image'
                             '/info_FILL0_wght400_GRAD0_opsz48.png">'
                             '<span class="popuptext_top" '
                             'id="infopopup_seq">'
                             '<b1>the DNA sequence</b1><br>'
                             '<b2>description</b2><br>'
                             '&emsp;Searches for this <br>'
                             '&emsp;sequence in the database<br>'
                             '<b2>Be aware of the following:</b2><br>'
                             '<ul>'
                             '<li>Searches are limited to ATCGN</li>'
                             '</ul>'
                             '<b2>Syntax-equivalent '
                             'in the normal search</b2><br>'
                             'AATGATGATGGCAGCGAN'
                             '</span>'),
                      render_kw={"placeholder": "Sequence"})
    eval_threshold = StringField(Markup('<button_eval_threshold '
                                        'class="info-button", '
                                        'onclick="infoPopUp_eval_threshold()",'
                                        'title="info">'
                                        '<img src = "../static/image/info_'
                                        'FILL0_wght400_GRAD0_opsz48.png">'
                                        '<span class="popuptext_top" '
                                        'id="infopopup_eval_threshold">'
                                        '<b1>the e value threshold</b1><br>'
                                        '<b2>description</b2><br>'
                                        '&emsp;uses this threshold <br>'
                                        '&emsp;to filter the max<br>'
                                        '&emsp;e value in the search <br>'
                                        '&emsp;results<br>'
                                        '<b2>Be aware of the following:</b2>'
                                        '<br>'
                                        '<ul>'
                                        '<li>filter values are limited '
                                        'to digets, e and -</li>'
                                        '</ul>'
                                        '<b2>Syntax-equivalent '
                                        'in the normal search</b2><br>'
                                        '1e-10'
                                        '</span>'),
                                 render_kw={"placeholder": "E-value threshold"
                                            })
    query_coverage = StringField(Markup('<button_query_coverage '
                                        'class="info-button", '
                                        'onclick="infoPopUp_query_coverage()",'
                                        'title="info">'
                                        '<img src = "../static/image/'
                                        'info_FILL0_wght400_GRAD0_opsz48.png">'
                                        '<span class="popuptext_top" '
                                        'id="infopopup_query_coverage">'
                                        '<b1>the query coverage'
                                        ' threshold</b1><br>'
                                        '<b2>description</b2><br>'
                                        '&emsp;uses this threshold <br>'
                                        '&emsp;to filter the max<br>'
                                        '&emsp;query coverage in the <br>'
                                        '&emsp;search results<br>'
                                        '<b2>Be aware of the following:</b2>'
                                        '<br>'
                                        '<ul>'
                                        '<li>filter values are limited '
                                        'to digets, e and -</li>'
                                        '</ul>'
                                        '<b2>Syntax-equivalent '
                                        'in the normal search</b2><br>'
                                        '1e-10'
                                        '</span>'),
                                 render_kw={"placeholder": "Query coverage"})
    submit = SubmitField('Search', render_kw={"class": "btn btn-primary"})
