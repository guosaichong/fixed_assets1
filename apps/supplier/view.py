from re import M
from flask import Blueprint, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.json import jsonify
from flask.templating import render_template
from sqlalchemy.sql.elements import not_
from sqlalchemy.sql.expression import or_
from .models import Machinepart, Supplier, db


supplier_bp = Blueprint("supplier", __name__)


@supplier_bp.route("/manage")
def manage():
    """
    管理页面
    """

    page = request.args.get("page", 1)

    pagination = db.session.query(Supplier).paginate(int(page), 15)

    return render_template("supplier/management.html", pagination=pagination)


@supplier_bp.route("/detail/<number>")
def detail(number):

    supplier_obj = db.session.query(Supplier).filter(
        Supplier.number == number).first()

    return render_template("supplier/detail.html", supplier_obj=supplier_obj)

# 增加前先验证编号是否唯一


@supplier_bp.route("/number_verifi/<number>", methods=["POST"])
def number_verifi(number):
    supplier_obj = db.session.query(Supplier).filter(
        Supplier.number == number).first()
    if supplier_obj:
        RET = {
            "code": 1,
            "msg": "供应商编号已存在"
        }
        return jsonify(RET)
    else:
        RET = {
            "code": 0,
            "msg": "供应商编号可以使用"
        }
        return jsonify(RET)


@supplier_bp.route("/add", methods=["GET", "POST"])
def add():
    """
    增加供应商
    """

    if request.method == "POST":
        number = request.form.get("number")
        name = request.form.get("name")

        supplier_obj = Supplier(number, name)
        db.session.add(supplier_obj)
        db.session.commit()
        RET = {
            "code": 0,
            "msg": "添加成功"
        }
        return jsonify(RET)

    return render_template("supplier/add.html")


@supplier_bp.route("/mod/<number>", methods=["GET", "POST"])
def mod(number):
    """
    修改供应商
    """
    supplier_obj = db.session.query(Supplier).filter(
        Supplier.number == number).first()
    if request.method == "POST":
        name = request.form.get("name")
        supplier_obj.name = name
        db.session.commit()
        RET = {
            "code": 0,
            "msg": "供应商修改成功"
        }
        return jsonify(RET)

    return render_template("supplier/mod.html", supplier_obj=supplier_obj)


@supplier_bp.route("/delete/<number>", methods=["GET", "POST"])
def delete(number):
    """
    删除供应商
    """
    # db.session.query(Supplier).filter(Supplier.number==number).first().machineparts.remove()
    supplier_obj = db.session.query(Supplier).filter(
        Supplier.number == number).first()

    db.session.delete(supplier_obj)
    db.session.commit()

    return redirect(url_for("supplier.manage"))


@supplier_bp.route("/add_machinepart/<number>", methods=["GET", "POST"])
def add_machinepart(number):
    """
    供应商增加零件
    """

    supplier_obj = db.session.query(Supplier).filter(
        Supplier.number == number).first()
    added_parts = supplier_obj.machineparts
    if request.method == "POST":
        part_number = request.form.get("part")
        # print(part_number)
        part_obj = db.session.query(Machinepart).filter(
            Machinepart.part_number == part_number).first()
        # print(part_obj)
        added_parts.append(part_obj)
        db.session.commit()
        RET = {
            "code": 0,
            "msg": "供应商增加零件成功"
        }
        return jsonify(RET)

    not_added_parts = db.session.query(Machinepart).filter(
        not_(Machinepart.id.in_([i.id for i in added_parts]))).all()

    return render_template("supplier/add_machinepart.html", supplier_obj=supplier_obj, added_parts=added_parts, not_added_parts=not_added_parts)

@supplier_bp.route("/reduce_machinepart/<number>", methods=["GET", "POST"])
def reduce_machinepart(number):
    """
    供应商减少零件
    """
    part_number=request.args.get("part_number",None)
    if part_number!=None:
        part_obj=db.session.query(Machinepart).filter(Machinepart.part_number==part_number).first()
        supplier_obj = db.session.query(Supplier).filter(
            Supplier.number == number).first()
        added_parts = supplier_obj.machineparts
        added_parts.remove(part_obj)
        db.session.commit()
        return redirect(url_for("supplier.add_machinepart",number=number))


@supplier_bp.route("/search", methods=["GET", "POST"])
def search():
    """查找功能"""
    if request.method == "POST":

        # find_content = request.form.get("search")
        # print(find_content)
        # pagination = db.session.query(Supplier).filter(or_(Supplier.number.like(
        #     f"%{find_content}%"), Supplier.name.like(f"%{find_content}%"))).paginate(1, 15)
        # return render_template("supplier/search.html", pagination=pagination, find_content=find_content)
        return {"code": 200, "msg": "ok"}

    find_content = request.args.get("find_content")
    page = request.args.get("page", 1)
    pagination = db.session.query(Supplier).filter(or_(Supplier.number.like(
        f"%{find_content}%"), Supplier.name.like(f"%{find_content}%"))).paginate(int(page), 15)
    return render_template("supplier/search.html", pagination=pagination,  find_content=find_content)
