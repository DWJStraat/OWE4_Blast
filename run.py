from waitress import serve
from __init__ import run
serve(run(), host="0.0.0.0", port=8080)