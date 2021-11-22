
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import text
from ..exts import db
# mysql 日期设置默认值必须使用timestamp类型
from sqlalchemy.sql.sqltypes import Boolean, Integer, TIMESTAMP, DateTime
from sqlalchemy.sql import func


class Visitor(db.Model):
    __tablename__ = 'visitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(16), nullable=False, index=True)
    license_number = db.Column(db.String(10), nullable=False)
    supplier = db.Column(db.String(30), nullable=False)
    logistics_company = db.Column(db.String(30), nullable=False)
    create_time = db.Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __init__(self, name, phone, license_number, supplier, logistics_company):
        self.name = name
        self.phone = phone
        self.license_number = license_number
        self.supplier = supplier
        self.logistics_company = logistics_company

    def __repr__(self):
        return "<Visitor(name:%s,phone:%s,license_number:%s,supplier:%s,logistics_company:%s)>" % (self.name, self.phone, self.license_number, self.supplier, self.logistics_company)


class UnloadingTime(db.Model):
    """
    记录一些时间，供用户选择，需要手动添加数据
    """
    __tablename__ = "unloading_time"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(DateTime, nullable=False)
    selected = db.Column(db.Boolean, server_default=text('0'), nullable=False)

class Unloading(db.Model):
    """
    预约卸货记录
    """
    __tablename__="unloading"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(16), nullable=False, index=True)
    license_number = db.Column(db.String(10), nullable=False)
    car_type_id=db.Column(db.Integer,db.ForeignKey("cartype.id"),nullable=False)
    unloading_time=db.Column(DateTime,nullable=False)
class CarType(db.Model):
    """
    货车车型
    """
    __tablename__="cartype"
    id=  db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(16), nullable=False)