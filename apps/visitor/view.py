from ..utils.generate_code import gene_code
from io import BytesIO
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify
from flask.globals import session
from flask.helpers import make_response, send_file
from ..exts.forms import AccessForm, AppointForm, CarForm
from ..exts import db,csrf
from .models import CarType, UnloadingTime2, Visitor, UnloadingTime, Unloading, Warehouse
from sqlalchemy import func
import logging
logger=logging.getLogger("root.visitor")

font = "../static/fonts/simkai.ttf"
visitor_bp = Blueprint("visitor", __name__)


@visitor_bp.route('/visitor', methods=["GET"])
def visitor_info():
    """查询访客信息"""
    date = request.args.get("date", datetime.date(datetime.now()))
    page = request.args.get("page", 1)
    pagination = db.session.query(Visitor).filter(db.cast(
        Visitor.create_time, db.DATE) == db.cast(date, db.DATE)).paginate(int(page), 15)

    return render_template("visitor/visitor_info.html", pagination=pagination, date=date)


@visitor_bp.route("/access", methods=["GET", "POST"])
def access():
    """
    访客填写来访信息
    """
    access_form = AccessForm()
    if access_form.validate_on_submit():
        visitor_info = access_form.data
        print(visitor_info)
        try:
            new_visitor = Visitor(name=visitor_info.get("visitor_name"), phone=visitor_info.get("phone"), license_number=visitor_info.get(
                "license_number"), supplier=visitor_info.get("supplier"), logistics_company=visitor_info.get("logistics_company"))
            db.session.add(new_visitor)

        except:
            db.session.rollback()
            return render_template("visitor/fail.html")
        db.session.commit()
        return render_template("visitor/success.html")
    return render_template("visitor/access.html", form=access_form)


@visitor_bp.route("/car", methods=["GET", "POST"])
def car():
    """
    一号库卸货窗口预约
    """
    car_form = CarForm()
    if car_form.validate_on_submit():
        car_info = car_form.data
        try:
            new_unloading = Unloading(supplier=car_info.get("supplier"), name=car_info.get("delivery_contact"), phone=car_info.get("phone"), license_number=car_info.get(
                "license_number"), car_type_id=car_info.get("car_type"), unloading_time=datetime.strptime(car_info.get("scheduled_unloading_time"), "%Y-%m-%d %H:%M:%S"),unloading_point_id=1)
            db.session.add(new_unloading)
            # 更新时间表，下次就不会再选这个时间了
            unloadingtime = UnloadingTime.query.filter(UnloadingTime.time == datetime.strptime(
                car_info.get("scheduled_unloading_time"), "%Y-%m-%d %H:%M:%S")).first()
            unloadingtime.selected = 1
        except:
            db.session.rollback()
            return render_template("visitor/unloading_fail.html")
        db.session.commit()
        return render_template("visitor/unloading_success.html")
    return render_template("visitor/car.html", form=car_form)

@visitor_bp.route("/appoint", methods=["GET", "POST"])
def appoint():
    """
    二号库卸货窗口预约
    """
    car_form = AppointForm()
    if car_form.validate_on_submit():
        car_info = car_form.data
        try:
            new_unloading = Unloading(supplier=car_info.get("supplier"), name=car_info.get("delivery_contact"), phone=car_info.get("phone"), license_number=car_info.get(
                "license_number"), car_type_id=car_info.get("car_type"), unloading_time=datetime.strptime(car_info.get("scheduled_unloading_time"), "%Y-%m-%d %H:%M:%S"),unloading_point_id=2)
            db.session.add(new_unloading)
            # 更新时间表，下次就不会再选这个时间了
            unloadingtime = UnloadingTime2.query.filter(UnloadingTime2.time == datetime.strptime(
                car_info.get("scheduled_unloading_time"), "%Y-%m-%d %H:%M:%S")).first()
            unloadingtime.selected = 1
        except:
            db.session.rollback()
            return render_template("visitor/unloading_fail.html")
        db.session.commit()
        return render_template("visitor/appoint_success.html")
    return render_template("visitor/appoint.html", form=car_form)


@visitor_bp.route('/unloading', methods=["GET"])
def unloading():
    """查询卸货约窗信息"""
    date = request.args.get("date", datetime.date(datetime.now()))
    page = request.args.get("page", 1)
    pagination = db.session.query(Unloading.supplier, Unloading.name, Unloading.phone, Unloading.license_number, CarType.name, Unloading.unloading_time,Warehouse.name).join(CarType, Unloading.car_type_id == CarType.id).join(Warehouse, Unloading.unloading_point_id == Warehouse.id).filter(db.cast(
        Unloading.unloading_time, db.DATE) == db.cast(date, db.DATE)).order_by(Unloading.unloading_time).paginate(int(page), 15)
    return render_template("visitor/unloading_info.html", pagination=pagination, date=date)


@visitor_bp.route("/access_code")
def get_access_code():
    """
    生成访客验证码，字符串写到session，图片传给前端
    """
    from ..utils.generate_code import gene_code
    font = "../static/fonts/simkai.ttf"
    image, code = gene_code((90, 30), 4, (255, 250, 240),
                            font, 25, (255, 0, 0), (190, 190, 190))
    # 将image对象转成二进制
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, "png")
    image_bytes = buffer.getvalue()
    # 将数据响应给前端
    response = make_response(image_bytes)
    response.headers["Content-Type"] = "image/png"
    session['access_code'] = code
    return response


@visitor_bp.route("/unloading_code")
def get_unloading_code():
    """
    生成卸货验证码，字符串写到session，图片传给前端
    """
    image, code = gene_code((90, 30), 4, (255, 250, 240),
                            font, 25, (255, 0, 0), (190, 190, 190))
    # 将image对象转成二进制
    buffer = BytesIO()
    image.save(buffer, "png")
    image_bytes = buffer.getvalue()
    # 将数据响应给前端
    response = make_response(image_bytes)
    response.headers["Content-Type"] = "image/png"
    session['unloading_code'] = code
    return response

@visitor_bp.route("/unloading_code2")
def get_unloading_code2():
    """
    生成二号库卸货验证码，字符串写到session，图片传给前端
    """
    image, code = gene_code((90, 30), 4, (255, 250, 240),
                            font, 25, (255, 0, 0), (190, 190, 190))
    # 将image对象转成二进制
    buffer = BytesIO()
    image.save(buffer, "png")
    image_bytes = buffer.getvalue()
    # 将数据响应给前端
    response = make_response(image_bytes)
    response.headers["Content-Type"] = "image/png"
    session['unloading_code2'] = code
    return response
