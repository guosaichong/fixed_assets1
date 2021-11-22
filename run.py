import os
import sys
from flask import request, render_template
from settings import DevelopConfig, ProductConfig, LOG_PATH,BASE_PATH
from apps import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.exts import db
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
handler = RotatingFileHandler(
    LOG_PATH+os.sep+"app.log", mode='a', maxBytes=10485760, backupCount=2, encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = create_app(DevelopConfig)
logger.info("app初始化成功")


@app.errorhandler(404)
def page_not_found(e):
    logger.warning("用户%s在请求%s页面时出错", request.remote_addr, request.url)
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    logger.warning("用户%s在请求%s页面时出错", request.remote_addr, request.url)
    return render_template('errors/500.html'), 500


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
