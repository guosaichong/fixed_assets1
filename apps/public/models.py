from sqlalchemy.orm import backref
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..exts import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.LargeBinary(65536), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    news_type_id = db.Column(
        db.Integer, db.ForeignKey("newstype.id"), nullable=False)
    create_time = db.Column(
        TIMESTAMP, server_default=func.now(), nullable=False)

    user = db.relationship("User", backref="news")
    news_type = db.relationship("NewsType", backref="news")

    def __init__(self,user_id, title, content,news_type_id):
        self.user_id=user_id
        self.title = title
        self.content = content
        self.news_type_id=news_type_id

class NewsType(db.Model):
    __tablename__ = "newstype"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
