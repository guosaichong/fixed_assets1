
from flask_bootstrap import Bootstrap

bootstrap=Bootstrap()

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

from flask_login import LoginManager

login_manager=LoginManager()
login_manager.login_view="/login"
login_manager.login_message="Please login first!"
login_manager.refresh_view="/login"
login_manager.needs_refresh_message="Refresh for login!"
login_manager.session_protection="strong"