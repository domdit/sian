import flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = flask.Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('SECRETKEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLDB')
app.config["MAIL_SERVER"] = "smtp.dreamhost.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAILUSER')
app.config["MAIL_PASSWORD"] = os.getenv('MAILPASS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message_category = 'info'

from siamsite import routes
from siamsite.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
