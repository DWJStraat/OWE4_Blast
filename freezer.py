"""
This file 'freezes' the app into a static site for use with (for example),
GitHub pages.
Created on 12-apr-2023 by David
Collaborators: David, Douwe, Jalmar
Last modified on 12-apr-2023 by David
"""
from flask_frozen import Freezer
from __init__ import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
