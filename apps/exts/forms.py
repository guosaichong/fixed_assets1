import datetime
from flask_wtf import FlaskForm
from wtforms.fields.core import DateField, SelectField, StringField
from wtforms.fields.simple import FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from flask import session
from ..exts import db
from ..visitor.models import CarType, UnloadingTime
from sqlalchemy import and_


class AccessForm(FlaskForm):
    """
    访客登记的表单
    """
    visitor_name = StringField("姓名:", validators=[DataRequired(), Length(2, 16, message="长度为2-16位"), Regexp(r"^(([a-zA-Z+\.?\·?a-zA-Z+]{2,16}$)|([\u4e00-\u9fa5+\·?\u4e00-\u9fa5+]{2,16}$))", message="格式不正确")],
                               render_kw={"placeholder": "请输入您的姓名", "class": "form-control"})
    phone = StringField("手机号:", validators=[DataRequired(), Length(11, 11, message="长度为11位"), Regexp(r"^1[3456789]\d{9}$", message="格式不正确")],
                        render_kw={"placeholder": "请输入您的手机号", "class": "form-control"})
    license_number = StringField("车牌号:", validators=[DataRequired(), Length(7, 10, message="长度为7-10位"), Regexp(r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$", message="格式不正确")],
                                 render_kw={"placeholder": "请输入您的车牌号", "class": "form-control"})
    supplier = StringField("供应商:", validators=[DataRequired(), Length(2, 30, message="长度为2-30位"), Regexp(r"^[\u4e00-\u9fa5A-Za-z0-9]{2,30}$", message="格式不正确")],
                           render_kw={"placeholder": "请输入您的供应商", "class": "form-control"})
    logistics_company = StringField("物流公司:", validators=[DataRequired(), Length(2, 30, message="长度为2-30位"), Regexp(r"^[\u4e00-\u9fa5A-Za-z0-9]{2,30}$", message="格式不正确")],
                                    render_kw={"placeholder": "请输入您的物流公司", "class": "form-control"})
    verify_code = StringField(label="验证码:", validators=[DataRequired()],
                              render_kw={"placeholder": "请输入验证码", "class": "form-control"})
    submit = SubmitField("提交", render_kw={"class": "form-control"})

    def validate_verify_code(self, field):
        # print(field.data)
        if session.get("access_code").lower() != self.verify_code.data.lower():
            raise ValidationError("验证码错误")


class CarForm(FlaskForm):
    """
    卸货登记的表单
    """

    def __init__(self):
        FlaskForm.__init__(self)
        unloading_time_list = UnloadingTime.query.filter(and_(UnloadingTime.time > datetime.datetime.now(
        ), UnloadingTime.time < datetime.datetime.now()+datetime.timedelta(days=7), UnloadingTime.selected == 0)).all()
        cartype_list = CarType.query.all()
        self.car_type.choices = [(i.id, i.name)for i in cartype_list]
        self.scheduled_unloading_time.choices = [
            (i.time, i.time)for i in unloading_time_list]
    supplier = StringField("供应商名称:", validators=[DataRequired(), Length(2, 30, message="长度为2-30位"), Regexp(r"^[\u4e00-\u9fa5A-Za-z0-9]{2,30}$", message="格式不正确")],
                           render_kw={"placeholder": "请输入您的供应商名称", "class": "form-control"})

    delivery_contact = StringField("送货联系人:", validators=[DataRequired(), Length(2, 16, message="长度为2-16位"), Regexp(r"^(([a-zA-Z+\.?\·?a-zA-Z+]{2,16}$)|([\u4e00-\u9fa5+\·?\u4e00-\u9fa5+]{2,16}$))", message="格式不正确")],
                                   render_kw={"placeholder": "请输入送货司机的姓名", "class": "form-control"})
    phone = StringField("送货手机号:", validators=[DataRequired(), Length(11, 11, message="长度为11位"), Regexp(r"^1[3456789]\d{9}$", message="格式不正确")],
                        render_kw={"placeholder": "请输入送货司机的手机号", "class": "form-control"})
    license_number = StringField("送货车牌号:", validators=[DataRequired(), Length(7, 10, message="长度为7-10位"), Regexp(r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$", message="格式不正确")],
                                 render_kw={"placeholder": "请输入送货司机的车牌号", "class": "form-control"})
    car_type = SelectField("送货车辆类型:", validators=[DataRequired()], render_kw={
                           "class": "form-control"}, coerce=int)
    # 预约卸货时间是从现在到往后10天的08:00,09:00,10:00,11:00,12:00,13:00,14:00,15:00,16:00,如果一个时间被用户选择，则这个时间就不能再被其他用户选择
    scheduled_unloading_time = SelectField("预约卸货时间", validators=[DataRequired()], render_kw={
                                           "class": "form-control"})

    verify_code = StringField(label="验证码:", validators=[DataRequired()],
                              render_kw={"placeholder": "请输入验证码", "class": "form-control"})
    submit = SubmitField("提交", render_kw={"class": "form-control"})

    def validate_verify_code(self, field):
        # print(field.data)
        if session.get("unloading_code").lower() != self.verify_code.data.lower():
            raise ValidationError("验证码错误")


class UploadForm(FlaskForm):
    """
    上传文件的表单
    """
    file = FileField(validators=[DataRequired()])
    submit = SubmitField(render_kw={"value": "上传", "class": "form-control"})
