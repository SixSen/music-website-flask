# 从模块的初始化文件中导入蓝图。
from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response
from . import admin
from app.models import Admin, Music
from app import db, app
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm

# 路由定义使用装饰器进行定义
@admin.route("/", methods=["GET", "POST"])
def index():
    """
    后台登录
    """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(admin_id=data["account"]).first()
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.admin_pwd == (data["pwd"]):
            flash("密码错误!", "err")
            return redirect(url_for("admin.index"))
        session["admin_id"] = admin.admin_id
        return redirect(url_for("admin.manage"))
    return render_template("admin/login.html", form=form)


@admin.route("/manage/")
def manage():
    admin_id = session.get("admin_id")
    return render_template("admin/index.html", id=admin_id)