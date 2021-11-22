
from ..exts import db
from flask_login import UserMixin
# mysql 日期设置默认值必须使用timestamp类型
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(18), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    create_time = db.Column(
        TIMESTAMP, server_default=func.now(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.id'), nullable=False, default=1)

    role = db.relationship("Role", backref="users")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return "<User(username: %s,email:%s,role:%s)>" % (self.username, self.email, self.role.name)


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(18), nullable=False, unique=True, index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(name:%s)>" % self.name
