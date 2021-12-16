
import os
from flask import Blueprint, render_template, jsonify, request
from flask.helpers import send_file
from settings import IMAGES_UPLOAD_PATH
from uuid import uuid4
from .models import News, NewsType
from ..user.view import role_required
from flask_login import login_required, current_user
from ..exts import db,csrf

public_bp = Blueprint("public", __name__)

# 网站小图标


@public_bp.route("/favicon.ico")
def get_favicon():
    return send_file("favicon.ico")
# 首页


@public_bp.route("/")
def index():
    industry = db.session.query(News).filter(
        News.news_type_id == 1).order_by(News.id.desc()).limit(5)
    industry_type_id = 1
    company = db.session.query(News).filter(
        News.news_type_id == 2).order_by(News.id.desc()).limit(5)
    company_type_id = 2
    notice = db.session.query(News).filter(
        News.news_type_id == 3).order_by(News.id.desc()).limit(5)
    notice_type_id = 3
    return render_template("public/index.html", industry=industry, company=company, notice=notice, industry_type_id=industry_type_id, company_type_id=company_type_id, notice_type_id=notice_type_id)

# 通知详情页


@public_bp.route("/news/<id>")
def news(id):
    news = db.session.query(News).get(id)
    news_list=db.session.query(News).order_by(News.id.desc()).all()
    return render_template("public/news.html", news=news,news_list=news_list)

# 管理员编辑页


@public_bp.route("/edit_news")
@login_required
@role_required
def edit_news():
    news_type_list = db.session.query(NewsType).all()
    return render_template("public/edit_news.html", news_type_list=news_type_list)

# 接收上传图片

@csrf.exempt
@public_bp.route("/upload_image", methods=["POST"])
def upload_image():
    upload_file = request.files.get("file")
    suffix = upload_file.filename.split(".")[-1]
    # print(suffix)
    filename = uuid4().hex+"."+suffix
    upload_file.save(IMAGES_UPLOAD_PATH+os.sep+filename)
    RET = {
        "location": request.host_url+"file/" + filename
    }
    return jsonify(RET)

@csrf.exempt
@public_bp.route("/publish_news", methods=["POST"])
@login_required
@role_required
def publish_news():
    user_id = current_user.id
    title = request.form.get("title")
    news_content = request.form.get("news-content")
    news_type = request.form.get("news-type")
    news = News(user_id=user_id, title=title,
                content=news_content.encode(), news_type_id=int(news_type))
    db.session.add(news)
    db.session.commit()
    # print(request.form.to_dict())
    return "发布成功！"


@public_bp.route("/file/<filename>")
def get_file(filename):
    return send_file(IMAGES_UPLOAD_PATH+os.sep+filename)

# 更多新闻列表页面


@public_bp.route("/news_list/<type>")
def news_list(type):
    page=request.args.get("page",1)
    pagination=db.session.query(News).filter(
        News.news_type_id == type).order_by(News.id.desc()).paginate(int(page), 15)
    return render_template("public/news_list.html",pagination=pagination,type=int(type))
