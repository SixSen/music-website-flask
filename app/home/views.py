from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response
from werkzeug.security import generate_password_hash
from . import home
from app.home.forms import LoginForm, RegisterForm
from app.models import User, Music, Board
from app import db, app, rd
import pymysql

#@ home = Blueprint("home",__name__)

# session.permantent = True




@home.route("/")
def index():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/index.html", page_data=page_data)

@home.route("/welcome/")
def welcome():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/welcome.html", name = session.get('user'), vclass =session.get('vclass'), page_data=page_data)

#登录
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if not user.check_pwd(data["pwd"]):
                flash("密码错误！", "err")
                return redirect(url_for("home.login"))
        else:
            flash("账户不存在！", "err")
            return redirect(url_for("home.login"))

        vclass = user.get_vclass()
        print(vclass)
        session["user"] = user.name
        session["user_id"] = user.id
        session["vclass"] = vclass

        return redirect(url_for("home.welcome"))
    return render_template("home/login.html", form=form)

# 退出
@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("vclass", None)
    return redirect(url_for('home.login'))

# 播放
@home.route("/play/")
def play():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    cursor = conn.cursor()
    musicd = int(request.args.get('id'))
    vclass = session.get('vclass')
    isbuy = 0
    sql = "SELECT free FROM music WHERE music_id = '%s' " % musicd
    cursor.execute(sql)
    results0 = cursor.fetchall()
    print(results0[0])
    for k in results0:
        if 1 == k[0]:
            isbuy = 1
    if vclass == 0:
        id = session.get('user_id')
        sql = "SELECT music_id FROM buy WHERE id = '%s' " % id
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)

        for rol in results:
            if musicd == rol[0]:
                isbuy = 1
        if isbuy == 1:
            return render_template("home/play.html", name=session.get('user'), user=session.get('user_id'), id=musicd)
        else:
            return "<h1>请购买此歌曲</h1>"
    else:
        return render_template("home/play.html", name=session.get('user'), user=session.get('user_id'), id=musicd)
# 注册
@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！", "ok")
    return render_template("home/register.html", form=form)


# 购买
@home.route("/buy")
def buy():
    return "buy"

# 搜索
@home.route("/search")
def search():
    key = request.args.get('key')
    print("key:",key)

    count = Music.query.filter(
        Music.music_name.ilike('%' + key + '%')
    ).count()

    page_data = Music.query.filter(
        Music.music_name.ilike('%' + key + '%')
    ).order_by(
        Music.listen.desc()
    )
    page_data.key = key
    print((page_data))

    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # cursor = conn.cursor()
    # sql = "SELECT * FROM music WHERE music_name = '%s' " % key
    #
    # cursor.execute(sql)
    # results = cursor.fetchall()
    # print(results)

    return render_template("home/search.html", name = session.get('user'),key=key,count= count, page_data=page_data)