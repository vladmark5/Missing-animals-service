from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_find.db'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'service/uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from service import route
