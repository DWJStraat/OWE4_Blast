from waitress import serve
import __init__ as app
serve(app, port=443, url_scheme='https')