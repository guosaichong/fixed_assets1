from flask import Blueprint, jsonify
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy.sql.elements import or_
from werkzeug.utils import redirect
from ..exts import db
from ..supplier.models import Machinepart

machine_bp = Blueprint("machinepart", __name__)


@machine_bp.route("/manage")
def manage():
    page = request.args.get("page", 1)

    pagination = db.session.query(Machinepart).paginate(int(page), 15)
    return render_template("machinepart/management.html", pagination=pagination)


@machine_bp.route("/detail/<part_number>")
def detail(part_number):

    machinepart_obj = db.session.query(Machinepart).filter(
        Machinepart.part_number == part_number).first()

    return render_template("machinepart/detail.html", machinepart_obj=machinepart_obj)

# 增加前先验证编号是否唯一


@machine_bp.route("/number_verifi/<part_number>", methods=["POST"])
def number_verifi(part_number):
    machinepart_obj = db.session.query(Machinepart).filter(
        Machinepart.part_number == part_number).first()
    if machinepart_obj:
        RET = {
            "code": 1,
            "msg": "零件编号已存在"
        }
        return jsonify(RET)
    else:
        RET = {
            "code": 0,
            "msg": "零件编号可以使用"
        }
        return jsonify(RET)


@machine_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        part_number = request.form.get("part_number")
        part_name = request.form.get("part_name")
        amount = int(request.form.get("amount"))
        
        low_storage = int(request.form.get("low_storage"))
        high_storage = int(request.form.get("high_storage"))
        quantifier = request.form.get("quantifier")
        machinepart_obj = Machinepart(
            part_number, part_name, amount, low_storage, high_storage, quantifier)
        db.session.add(machinepart_obj)
        db.session.commit()
        RET = {
            "code": 0,
            "msg": "添加成功"
        }
        return jsonify(RET)

    return render_template("machinepart/add.html")


@machine_bp.route("/mod/<part_number>", methods=["GET", "POST"])
def mod(part_number):
    machinepart_obj = db.session.query(Machinepart).filter(
        Machinepart.part_number == part_number).first()
    if request.method == "POST":
        part_name = request.form.get("part_name")
        amount = int(request.form.get("amount"))
        quantifier = request.form.get("quantifier")
        low_storage = int(request.form.get("low_storage"))
        high_storage = int(request.form.get("high_storage"))
        print(request.form.to_dict())
        
        machinepart_obj.part_name = part_name
        machinepart_obj.amount = amount
        machinepart_obj.quantifier = quantifier
        machinepart_obj.low_storage = low_storage
        machinepart_obj.high_storage = high_storage
        db.session.commit()
        RET = {
            "code": 0,
            "msg": "修改成功"
        }
        return jsonify(RET)
    return render_template("machinepart/mod.html", machinepart_obj=machinepart_obj)


@machine_bp.route("/delete/<part_number>", methods=["GET"])
def delete(part_number):
    machinepart_obj=db.session.query(Machinepart).filter(Machinepart.part_number==part_number).first()
    db.session.delete(machinepart_obj)
    db.session.commit()
    return redirect(url_for("machinepart.manage"))


@machine_bp.route("/search", methods=["GET", "POST"])
def search():
    """查找功能"""
    if request.method == "POST":

        # find_content = request.form.get("search")
        # pagination = db.session.query(Machinepart).filter(or_(Machinepart.part_number.like(
        #     f"%{find_content}%"), Machinepart.part_name.like(f"%{find_content}%"))).paginate(1, 15)
        # return render_template("machinepart/search.html", pagination=pagination, find_content=find_content)
        return {"code":200,"msg":"ok"}
    find_content = request.args.get("find_content")
    page = request.args.get("page", 1)
    pagination = db.session.query(Machinepart).filter(or_(Machinepart.part_number.like(
        f"%{find_content}%"), Machinepart.part_name.like(f"%{find_content}%"))).paginate(int(page), 15)
    return render_template("machinepart/search.html", pagination=pagination,  find_content=find_content)
