"""
Uses waitress to serve the app on port 5000
"""

from waitress import serve
import __init__ as app

serve(app.app, host='0.0.0.0', port=5000)
