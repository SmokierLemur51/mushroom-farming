from flask_bcrypt import Bcrypt
from flask_login import LoginManager

fbcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"
