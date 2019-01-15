# 从模块的初始化文件中导入蓝图。
from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response, abort
from . import admin
from app.models import User, Music, Board, Buy, db, Library, Admin
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


@admin.route("/logout/")
def logout():
    session.pop("admin_id", None)
    return redirect(url_for('admin.index'))

@admin.route("/manage/")
def manage():
    if not "admin_id" in session:
        return abort(404)
    admin_id = session.get("admin_id")
    return render_template("admin/index.html", id=admin_id)

@admin.route("/all/")
def all():
    if not "admin_id" in session:
        return abort(404)
    form = User.query.all()
    print(form)
    admin_id = session.get("admin_id")
    return render_template("admin/all.html", id=admin_id ,form = form)

@admin.route("/deuser/")
def deuser():
    if not "admin_id" in session:
        return abort(404)
    uid = int(request.args.get("id"))
    form = User.query.all()
    admin_id = session.get("admin_id")
    user = User.query.filter(User.id==uid).first()
    # print(musicd)
    db.session.delete(user)
    db.session.commit()
    flash("已经成功注销id为%d的用户" % uid, "ok")
    return redirect(url_for('admin.all'))