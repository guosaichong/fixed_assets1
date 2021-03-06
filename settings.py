import os


class DevelopConfig:
    ENV = "development"
    DEBUG = True
    # mysql配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:123456@localhost/fixed_assets?charset=utf8mb4"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    # 设定连接池的连接超时时间。默认是 10 。
    SQLALCHEMY_POOL_TIMEOUT = 10
    # 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定这个值为 2 小时。
    SQLALCHEMY_POOL_RECYCLE = 7200
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session
    SECRET_KEY = "!@#$QWER"
    # 上传文件大小限制
    MAX_CONTENT_LENGTH = 2*1024*1024


class ProductConfig:
    ENV = "production"
    DEBUG = False
    # mysql配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://用户名:密码@主机地址/fixed_assets?charset=utf8mb4"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    # 设定连接池的连接超时时间。默认是 10 。
    SQLALCHEMY_POOL_TIMEOUT = 10
    # 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定这个值为 2 小时。
    SQLALCHEMY_POOL_RECYCLE = 7200
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session
    SECRET_KEY = "!@#$QWER"
    # 上传文件大小限制
    MAX_CONTENT_LENGTH = 2*1024*1024


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_PATH, "logs")
IMAGES_UPLOAD_PATH = os.path.join(BASE_PATH, "images_upload")
File_UPLOAD_PATH = os.path.join(BASE_PATH, "files_upload")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
if not os.path.exists(IMAGES_UPLOAD_PATH):
    os.mkdir(IMAGES_UPLOAD_PATH)
if not os.path.exists(File_UPLOAD_PATH):
    os.mkdir(File_UPLOAD_PATH)
if not os.path.exists(os.path.join(File_UPLOAD_PATH, "办公软件")):
    os.mkdir(os.path.join(File_UPLOAD_PATH, "办公软件"))
if not os.path.exists(os.path.join(File_UPLOAD_PATH, "常用文件")):
    os.mkdir(os.path.join(File_UPLOAD_PATH, "常用文件"))
if not os.path.exists(os.path.join(File_UPLOAD_PATH, "临时文件")):
    os.mkdir(os.path.join(File_UPLOAD_PATH, "临时文件"))
# 新浪邮箱设置
HOST = 'smtp.sina.com'
PORT = 465
ACCOUNT = 'gsc21@sina.com'
PASSWORD = '926f94947f38a12c'
