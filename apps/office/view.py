from ..user.view import role_required
from sqlalchemy import or_
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for
from flask import request, jsonify
from flask.templating import render_template
from .models import Equipment, Category, Department, Location
from ..exts import db,csrf
import logging
logger = logging.getLogger("root.office")

office_bp = Blueprint("office", __name__)


# 增加前先验证资产编号是否唯一
@csrf.exempt
@office_bp.route("/asset_number_verifi/<asset_number>", methods=["POST"])
def asset_number_verifi(asset_number):
    equ_obj = db.session.query(Equipment).filter(
        Equipment.asset_number == asset_number).first()
    if equ_obj:
        RET = {
            "code": 1,
            "msg": "资产编号已存在"
        }
        return jsonify(RET)
    else:
        RET = {
            "code": 0,
            "msg": "资产编号可以使用"
        }
        return jsonify(RET)

@csrf.exempt
@office_bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required
def add():
    if request.method == "POST":
        # print(request.form.to_dict())
        name = request.form.get("name")
        asset_number = request.form.get("asset_number")
        asset_status = request.form.get("asset_status")
        department_id = request.form.get("department")
        category_id = request.form.get("category")
        location_id = request.form.get("location")
        equ = Equipment(name, asset_number, asset_status,
                        department_id, category_id, location_id)
        equ.model = request.form.get("model")
        equ.parameter = request.form.get("parameter")
        equ.user = request.form.get("user")
        equ.IPaddress = request.form.get("IPaddress")
        equ.purchase_date = request.form.get("purchase_date")
        equ.purchase_cost = request.form.get("purchase_cost")
        try:
            db.session.add(equ)

            RET = {
                "code": 0,
                "msg": "添加成功"
            }
            # print(current_user.username)
            logger.info("%s成功添加%s", current_user.username, asset_number)
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "添加失败,请重新提交。"
            }
            logger.info("%s添加%s失败", current_user.username, asset_number)
        db.session.commit()
        return jsonify(RET)
    category_id = request.args.get("category")
    category_list = Category.query.order_by(Category.id).all()
    dep_list = Department.query.all()
    loc_list = Location.query.all()
    cat_name = db.session.query(Category.name).filter(
        Category.id == int(category_id)).first()
    return render_template("office/add.html", category_list=category_list, category_id=int(category_id), dep_list=dep_list, loc_list=loc_list, cat_name=cat_name[0])

@csrf.exempt
@office_bp.route("/dep_add", methods=["GET", "POST"])
@login_required
@role_required
def dep_add():
    if request.method == "POST":
        # print(request.form.to_dict())
        name = request.form.get("name")
        asset_number = request.form.get("asset_number")
        asset_status = request.form.get("asset_status")
        department_id = request.form.get("department")
        category_id = request.form.get("category")
        location_id = request.form.get("location")
        equ = Equipment(name, asset_number, asset_status,
                        department_id, category_id, location_id)
        equ.model = request.form.get("model")
        equ.parameter = request.form.get("parameter")
        equ.user = request.form.get("user")
        equ.IPaddress = request.form.get("IPaddress")
        equ.purchase_date = request.form.get("purchase_date")
        equ.purchase_cost = request.form.get("purchase_cost")
        try:
            db.session.add(equ)

            RET = {
                "code": 0,
                "msg": "添加成功"
            }
            # print(current_user.username)
            logger.info("%s成功添加%s", current_user.username, asset_number)
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "添加失败,请重新提交。"
            }
            logger.info("%s添加%s失败", current_user.username, asset_number)
        db.session.commit()
        return jsonify(RET)
    department_id = request.args.get("department")
    category_list = Category.query.order_by(Category.id).all()
    cat_list = Category.query.all()
    loc_list = Location.query.all()
    return render_template("office/dep_add.html", category_list=category_list, department_id=int(department_id), cat_list=cat_list, loc_list=loc_list)

# 按位置添加设备

@csrf.exempt
@office_bp.route("/loc_add", methods=["GET", "POST"])
@login_required
@role_required
def loc_add():
    if request.method == "POST":
        # print(request.form.to_dict())
        name = request.form.get("name")
        asset_number = request.form.get("asset_number")
        asset_status = request.form.get("asset_status")
        department_id = request.form.get("department")
        category_id = request.form.get("category")
        location_id = request.form.get("location")
        equ = Equipment(name, asset_number, asset_status,
                        department_id, category_id, location_id)
        equ.model = request.form.get("model")
        equ.parameter = request.form.get("parameter")
        equ.user = request.form.get("user")
        equ.IPaddress = request.form.get("IPaddress")
        equ.purchase_date = request.form.get("purchase_date")
        equ.purchase_cost = request.form.get("purchase_cost")
        try:
            db.session.add(equ)

            RET = {
                "code": 0,
                "msg": "添加成功"
            }
            # print(current_user.username)
            logger.info("%s成功添加%s", current_user.username, asset_number)
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "添加失败,请重新提交。"
            }
            logger.info("%s添加%s失败", current_user.username, asset_number)
        db.session.commit()
        return jsonify(RET)
    location_id = request.args.get("location")
    category_list = Category.query.order_by(Category.id).all()
    cat_list = Category.query.all()
    dep_list = Department.query.all()

    return render_template("office/loc_add.html", category_list=category_list, location_id=int(location_id), cat_list=cat_list, dep_list=dep_list)


@office_bp.route("/detail")
def detail():
    category_list = Category.query.order_by(Category.id).all()
    dep_list = Department.query.all()
    loc_list = Location.query.all()
    category_id_list = []
    for category in category_list:
        category_id_list.append(category.id)
    category_id = request.args.get("category", 1)
    try:
        if int(category_id) not in category_id_list:
            return redirect(url_for('office.detail'))
    except:
        return redirect(url_for('office.detail'))
    else:
        page = request.args.get("page", 1)

        pagination = db.session.query(Equipment).filter(
            Equipment.category_id == int(category_id)).paginate(int(page), 15)

        cat_name = db.session.query(Category.name).filter(
            Category.id == int(category_id)).first()
        return render_template("office/detail.html", pagination=pagination, category_list=category_list, dep_list=dep_list, loc_list=loc_list,
                               category_id=int(category_id), category_id_list=category_id_list, cat_name=cat_name[0])

# 按部门 详情列表


@office_bp.route("/department")
def department():
    department_id = request.args.get("department", 1)
    dep_list = Department.query.all()
    dep_id_list = []
    for dep in dep_list:
        dep_id_list.append(dep.id)
    # print(dep_id_list)
    try:
        if int(department_id) not in dep_id_list:
            return redirect(url_for('office.department'))
    except:
        return redirect(url_for('office.department'))
    else:
        page = request.args.get("page", 1)
        pagination = db.session.query(Equipment).filter(
            Equipment.department_id == int(department_id)).paginate(int(page), 15)

        category_list = Category.query.order_by(Category.id).all()

        loc_list = Location.query.all()
        department_name = db.session.query(Department.name).filter(
            Department.id == int(department_id)).first()
        return render_template("office/department.html", pagination=pagination, category_list=category_list, dep_list=dep_list, loc_list=loc_list,
                               department_id=int(department_id), department_name=department_name[0], dep_id_list=dep_id_list)

# 按位置 详情列表


@office_bp.route("/location")
def location():
    location_id = request.args.get("location", 1)
    loc_list = Location.query.all()
    loc_id_list = []
    for loc in loc_list:
        loc_id_list.append(loc.id)
    try:
        if int(location_id) not in loc_id_list:
            return redirect(url_for('office.location'))
    except:
        return redirect(url_for('office.location'))
    else:
        page = request.args.get("page", 1)
        pagination = db.session.query(Equipment).filter(
            Equipment.location_id == int(location_id)).paginate(int(page), 15)

        category_list = Category.query.order_by(Category.id).all()
        dep_list = Department.query.all()

        location_name = db.session.query(Location.name).filter(
            Location.id == int(location_id)).first()
        return render_template("office/location.html", pagination=pagination, category_list=category_list, dep_list=dep_list, loc_list=loc_list,
                               location_id=int(location_id), location_name=location_name[0])


# 修改信息
@csrf.exempt
@office_bp.route("/mod/<asset_number>", methods=["GET", "POST"])
@login_required
@role_required
def mod(asset_number):
    if request.method == "POST":
        # print(request.form.to_dict())
        name = request.form.get("name")
        model = request.form.get("model")
        parameter = request.form.get("parameter")
        department_id = request.form.get("department")
        location_id = request.form.get("location")
        user = request.form.get("user")
        IPaddress = request.form.get("IPaddress")
        purchase_date = request.form.get("purchase_date")
        purchase_cost = request.form.get('purchase_cost')
        asset_status = request.form.get("asset_status")
        try:
            Equipment.query.filter(Equipment.asset_number == asset_number).update({"name": name, "model": model, "parameter": parameter, "user": user, "IPaddress": IPaddress,
                                                                                   "asset_status": asset_status, "department_id": department_id, "location_id": location_id, "purchase_date": purchase_date, "purchase_cost": purchase_cost})

            RET = {
                "code": 0,
                "msg": "修改成功"
            }
            logger.info("%s成功修改%s", current_user.username, asset_number)
        except:
            db.session.rollback()
            RET = {
                "code": 1,
                "msg": "修改失败"
            }
            logger.info("%s修改%s失败", current_user.username, asset_number)
        db.session.commit()
        return jsonify(RET)
    else:
        res = db.session.query(Equipment.name, Equipment.model, Equipment.parameter, Department.name, Location.name, Equipment.user, Equipment.IPaddress, Equipment.purchase_date, Equipment.purchase_cost, Equipment.asset_status, Equipment.category_id).join(Department, Equipment.department_id == Department.id).join(Location, Equipment.location_id == Location.id).filter(
            Equipment.asset_number == asset_number).first()
        category_list = Category.query.order_by(Category.id).all()
        dep_list = db.session.query(Department).all()
        loc_list = db.session.query(Location).all()
        category_id = db.session.query(Equipment.category_id).filter(
            Equipment.asset_number == asset_number).first()
        return render_template("office/mod.html", res=res, asset_number=asset_number, dep_list=dep_list, loc_list=loc_list, category_list=category_list, category_id=category_id[0])

# 删除功能


@office_bp.route("/delete/<asset_number>")
@login_required
@role_required
def delete(asset_number):
    category_id = db.session.query(Equipment.category_id).filter(
        Equipment.asset_number == asset_number).first()
    Equipment.query.filter(Equipment.asset_number == asset_number).delete()
    db.session.commit()
    logger.warning("%s删除了%s", current_user.username, asset_number)
    return redirect("/detail"+"?category="+str(category_id[0]))

@csrf.exempt
@office_bp.route("/search", methods=["GET", "POST"])
def search():
    """查找功能"""
    if request.method == "POST":
        category_list = Category.query.order_by(Category.id).all()
        dep_list = Department.query.all()
        loc_list = Location.query.all()
        find_content = request.form.get("search")
        pagination = db.session.query(Equipment).filter(or_(Equipment.asset_number.like(
            f"%{find_content}%"), Equipment.name.like(f"%{find_content}%"))).paginate(1, 15)
        return render_template("office/search.html", pagination=pagination, category_list=category_list, find_content=find_content, dep_list=dep_list, loc_list=loc_list)
    category_list = Category.query.order_by(Category.id).all()
    dep_list = Department.query.all()
    loc_list = Location.query.all()
    find_content = request.args.get("find_content")
    page = request.args.get("page", 1)
    pagination = db.session.query(Equipment).filter(or_(Equipment.asset_number.like(
        f"%{find_content}%"), Equipment.name.like(f"%{find_content}%"))).paginate(int(page), 15)
    return render_template("office/search.html", pagination=pagination, category_list=category_list, find_content=find_content, dep_list=dep_list, loc_list=loc_list)
