
from functools import wraps
from flask_login.utils import login_required, login_user, logout_user, current_user
from ..office.models import Category, Department, Equipment, Location
from flask.helpers import flash, url_for
from ..exts import db, login_manager,csrf
from .models import Role, User
from flask import Blueprint, jsonify, redirect, session
from flask.globals import request
from flask.templating import render_template
import math
import logging
logger = logging.getLogger("root.user")

user_bp = Blueprint("user", __name__)


def role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        role_id = current_user.role.id
        if role_id >= 2:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.role"))
    return decorated_view


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username == username).first()
        if user.password == password:
            # 记录用户登录状态
            login_user(user)
            # session['_user_id'] = user_id-> user_id=getattr(user, current_app.login_manager.id_attribute)()->LoginManager(object)中self.id_attribute = ID_ATTRIBUTE
            # ID_ATTRIBUTE = 'get_id'-> getattr(user, "get_id")()=user.get_id()->用户模型类中的get_id() return text_type(self.id)->text_type(self.id)=str(user.id)->session["_user_id"]="id值"
            RET = {
                "code": 200,
                "msg": "登录成功",
            }
            logger.info("%s登录成功", current_user.username)
        else:

            RET = {
                "code": 201,
                "msg": "密码错误"
            }
            logger.info("%s登录失败", username)
        return jsonify(RET)

    return render_template("user/login.html")

@csrf.exempt
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        user = User(username, password, email)
        db.session.add(user)
        db.session.commit()
        RET = {
            "code": 200,
            "msg": "注册成功"
        }
        logger.info("新用户%s注册成功", username)
        return jsonify(RET)
    return render_template("user/register.html")

# 退出


@user_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logger.info("%s用户退出", current_user.username)
    logout_user()
    return redirect("/")


# 验证用户名
@csrf.exempt
@user_bp.route("/verifi_username", methods=["POST"])
def verifi_username():
    username = request.form.get("username")
    user = User.query.filter(User.username == username).first()
    if user == None:
        RET = {
            "code": 4000,
            "msg": "用户不存在"
        }

    else:
        RET = {
            "code": 4001,
            "msg": "用户已存在"
        }
    return jsonify(RET)

# 验证密码


@user_bp.route("/verifi_password", methods=["POST"])
def verifi_password():
    password = request.form.get("password")
    username = request.form.get("username")
    user_obj = User.query.filter(User.username == username).first()
    if not user_obj.password == password:
        RET = {
            "code": 0,
            "msg": "密码错误"
        }
        return jsonify(RET)
    RET = {
        "code": 1,
        "msg": "密码正确"
    }
    return jsonify(RET)


@user_bp.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        user = User.query.filter_by(username=username).first()
        # print(user.email)
        if user.email != email:
            RET = {
                "code": 2,
                "msg": "您输入的预留邮箱不正确！"
            }

            return jsonify(RET)
        # 生成随机8个字符作为新密码
        import string
        import random
        goal = ''.join(random.sample(string.ascii_letters+string.digits, 8))
        # print(goal)
        # 将新密码通过邮件发给用户
        from ..utils.email_serve import mail

        if mail(email, "忘记密码", "请使用如下密码登录："+goal):
            import hashlib

            password_md5 = hashlib.md5(
                goal.encode(encoding="utf-8")).hexdigest()
            # print(password_md5)
            User.query.filter_by(username=username).update(
                {"password": password_md5})
            db.session.commit()
            RET = {
                "code": 0,
                "msg": "请进入邮箱查看新密码"
            }
            return jsonify(RET)
    return render_template("user/forget.html")


@user_bp.route("/mod_password", methods=["GET", "POST"])
@login_required
def mod_password():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            User.query.filter(User.username == username).update(
                {"password": password})
            RET = {
                "code": 0,
                "msg": "修改成功，请重新登录！"
            }
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "修改失败"
            }
        db.session.commit()
        return jsonify(RET)
    category_list = Category.query.order_by(Category.id).all()
    return render_template("user/mod_password.html", category_list=category_list)


@user_bp.route("/info", methods=["GET", "POST"])
@login_required
def info():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        try:
            db.session.query(User).filter(
                User.username == username).update({"email": email})
            RET = {
                "code": 0,
                "msg": "修改成功"
            }
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "修改失败"
            }
        db.session.commit()
        return jsonify(RET)
    category_list = Category.query.order_by(Category.id).all()
    return render_template("user/info.html", category_list=category_list)


@user_bp.route("/role", methods=["GET", "POST"])
@login_required
def role():
    if request.method == "POST":
        pass
    category_list = Category.query.order_by(Category.id).all()
    return render_template("user/role.html", category_list=category_list)
