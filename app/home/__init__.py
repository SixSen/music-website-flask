# _*_ coding: utf-8 _*_

from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views


# from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response
# from werkzeug.security import generate_password_hash
# # import app.home.views as views
# import app.home.forms as forms
# from app.models import User
# from app import db, app, rd
# home = Blueprint("home",__name__)
#
# @home.route("/")
# def index():
#     return render_template("home/index.html")
#
# #登录
# @home.route("/login/", methods=["GET", "POST"])
# def login():
#     form = forms.LoginForm()
#     if form.validate_on_submit():
#         data = form.data
#         user = User.query.filter_by(name=data["name"]).first()
#         if user:
#             if not user.check_pwd(data["pwd"]):
#                 flash("密码错误！", "err")
#                 return redirect(url_for("home.login"))
#         else:
#             flash("账户不存在！", "err")
#             return redirect(url_for("home.login"))
#         session["user"] = user.name
#         session["user_id"] = user.id
#         return redirect(url_for("home.index"))
#     return render_template("home/login.html", form=form)
#
# # 退出
# @home.route("/logout/")
# def logout():
#     return redirect(url_for('home.login'))
#
# # 会员注册
# @home.route("/register/", methods=["GET", "POST"])
# def register():
#     form = forms.RegisterForm()
#     if form.validate_on_submit():
#         data = form.data
#         user = User(
#             name=data["name"],
#             email=data["email"],
#             phone=data["phone"],
#             pwd=generate_password_hash(data["pwd"]),
#         )
#         db.session.add(user)
#         db.session.commit()
#         flash("注册成功！", "ok")
#     return render_template("home/register.html", form=form)