from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:////tmp/schema.sql')
app.config['MAX_CONTENT_LENGTH'] = 524288000
app.config['SECRET_KEY'] = "imdgf"
app.config['DEBUG'] = False
admin = Admin(app, name='Archiver')
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


@app.before_first_request
def create_user():
    db.create_all()


import archiver.views
