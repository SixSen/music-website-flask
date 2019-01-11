from app import app
import sys
import os
from flask_script import Manager
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.join(BASE_DIR, 'movie_project\\app'))
# sys.path.insert(0, os.path.join(BASE_DIR, 'movie_project\\app\\admin'))
# sys.path.insert(0, os.path.join(BASE_DIR, 'movie_project\\app\\home'))

manage = Manager(app)

if __name__ == "__main__":
    manage.run()
