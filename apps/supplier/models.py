from ..exts import db
from sqlalchemy import text

# 供应商和零件表，一个供应商可以供应多个零件，一个零件可以由多个供应商供应，多对多的关系，多对多需要第三张表
supplier_to_machinepart = db.Table("supplier_to_machinepart", db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id'), primary_key=True),
                                   db.Column('machinepart_id', db.Integer, db.ForeignKey('machinepart.id'), primary_key=True))

# class SupplierToMachinepart(db.Model):
#     __tablename__="supplier_to_machinepart"
#     supplier_id=db.Column(db.Integer,db.ForeignKey("supplier.id"), primary_key=True)
#     machinepart_id=db.Column(db.Integer,db.ForeignKey("machinepart.id"), primary_key=True)


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    number = db.Column(
        db.String(30), nullable=False, index=True, unique=True)
    machineparts = db.relationship(
        "Machinepart", secondary=supplier_to_machinepart, backref='suppliers')

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return "<Supplier(supplier_number:%s,supplier_name:%s)>" % (self.number, self.name)


class Machinepart(db.Model):
    __tablename__ = "machinepart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    part_number = db.Column(
        db.String(20), nullable=False, index=True, unique=True)
    part_name = db.Column(db.String(30), nullable=False)
    # Integer,Boolean类型设置默认值需要from sqlalchemy import text text("字符串")
    amount = db.Column(db.Integer, server_default=text("0"), nullable=False)
    low_storage = db.Column(
        db.Integer, server_default=text("1"), nullable=False)
    high_storage = db.Column(
        db.Integer, server_default=text("999999"), nullable=False)
    quantifier = db.Column(db.String(10), nullable=False)

    def __init__(self, part_number, part_name, amount, low_storage, high_storage, quantifier):
        self.part_number = part_number
        self.part_name = part_name
        self.amount = amount
        self.low_storage = low_storage
        self.high_storage = high_storage
        self.quantifier = quantifier

    def __repr__(self):
        return "<Machinepart(part_number:%s,part_name:%s,amount:%d,low_storage:%d,high_storage:%d,quantifier:%s)>" % (self.part_number, self.part_name, self.amount, self.low_storage, self.high_storage, self.quantifier)
