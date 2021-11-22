from ..exts import db


# 部门和办公设备的关系 一个部门可以使用多个办公设备 一个办公设备只能被一个部门使用 一对多的关系
class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)
    leader = db.Column(db.String(10), nullable=False, index=True)

    def __init__(self, name, leader):
        self.name = name
        self.leader = leader

    def __repr__(self):
        return "<Department(name:%s,leader:%s)>" % (self.name, self.leader)


# 类别和办公设备的关系 一个类别可以有多个办公设备 一个办公设备只能属于一个类别 一对多的关系
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category(name:%s)>" % (self.name)


# 存放位置和办公设备的关系 一对多的关系
class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Location(name:%s)>" % (self.name)


class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False, index=True)
    model = db.Column(db.String(20))
    parameter = db.Column(db.String(30))
    user = db.Column(db.String(30))
    IPaddress = db.Column(db.String(20))
    asset_number = db.Column(db.String(20), nullable=False, unique=True)
    asset_status = db.Column(db.Enum("在用", "闲置", "报废", "转移"), nullable=False)
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Float)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'location.id'), nullable=False)

    department = db.relationship("Department", backref="equipments")
    category = db.relationship("Category", backref="equipments")
    location = db.relationship("Location", backref="equipments")

    def __init__(self, name, asset_number, asset_status, department_id, category_id, location_id):
        self.name = name
        self.asset_number = asset_number
        self.asset_status = asset_status
        self.department_id = department_id
        self.category_id = category_id
        self.location_id = location_id

    def __repr__(self):
        return "<Equipment(name:%s,asset_number:%s,asset_status:%s)>" % (self.name, self.asset_number, self.asset_status)
