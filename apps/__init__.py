
from .utils.get_sth import get_months
from .utils.content_serve import byte2str,datetime2date
from .office.view import office_bp
from .public.view import public_bp
from .user.view import user_bp
from .upload.view import upload_bp
from .visitor.view import visitor_bp
from flask import Flask
from .exts import bootstrap,db,login_manager


def create_app(class_name):
    
    app=Flask(__name__)
    app.config.from_object(class_name)
    # 注册扩展
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 添加全局模板
    app.add_template_global(get_months,"get_months")
    app.add_template_global(byte2str,"byte2str")
    app.add_template_global(datetime2date,"datetime2date")
    # 注册蓝图
    app.register_blueprint(office_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(visitor_bp)
    app.register_blueprint(upload_bp)
    print(app.url_map)
    return app