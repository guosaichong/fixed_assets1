
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

csrf=CSRFProtect()
bootstrap = Bootstrap()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message = "Please login first!"
login_manager.refresh_view = "/login"
login_manager.needs_refresh_message = "Refresh for login!"
login_manager.session_protection = "strong"
