import os
# from config.base_config import SQLALCHEMY_DATABASE_URI

__author__ = 'mtianyan'
__date__ = '2017/8/26 17:05'
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

app = Flask(__name__)
# 使用app对象，调用register_blueprint函数进行蓝图的注册
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# 用于连接数据的数据库。
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:1232123@127.0.0.1:3306/musicdb"

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:nucoj@39.106.214.230:3306/musicdb"
app.debug = True
# Secret_key用于密码加盐与CSRF验证
app.secret_key = "Sixsense1212qwqwasas"

app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")
db = SQLAlchemy(app)
rd = FlaskRedis(app)
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
# 第一个参数是蓝图，第二个参数是url地址的前缀。通过地址前缀划分前后台的路由
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404