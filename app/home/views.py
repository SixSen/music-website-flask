from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response
from werkzeug.security import generate_password_hash
from . import home
from app.home.forms import LoginForm, RegisterForm, UserdetailForm, PwdForm
from app.models import User, Music, Board, Buy, db
# from app import db, app, rd
import pymysql


# pymysql的数据库连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')

# conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
# @ home = Blueprint("home",__name__)
# session.permantent = True


# 根路由
@home.route("/")
def index():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/index.html", page_data=page_data)


# 登陆后的欢迎主页
@home.route("/welcome/")
def welcome():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/welcome.html", name=session.get('user'), vclass=session.get('vclass'), page_data=page_data)


# 登录
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


# 退出登录
@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("vclass", None)
    flash("您已成功登出！", "ok")
    return redirect(url_for('home.login'))


# 个人中心
@home.route("/user/", methods=["GET", "POST"])
# @user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session["user_id"]))
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
    if form.validate_on_submit():
        data = form.data
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在！", "err")
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在！", "err")
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("手机号码已经存在！", "err")
            return redirect(url_for("home.user"))

        user.name = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        db.session.add(user)
        db.session.commit()
        flash("修改成功！", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", name=session.get('user'), form=form, user=user)

# 密码修改
@home.route("/pwd/", methods=["GET", "POST"])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误！", "err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html",name=session.get('user'),  form=form)

# 订阅会员
@home.route("/sub/", methods=["GET", "POST"])
def sub():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误！", "err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout'))
    return render_template("home/subscribe.html",name=session.get('user'),  form=form)

# 播放音乐
@home.route("/play/")
def play():
    if session.get('user') is None:
        flash("请先登录才能播放音乐", "err")
        return redirect(url_for('home.login'))
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
            flash('请先购买此歌曲或订阅会员-err:%d' % musicd)
            return render_template("home/msg.html")
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
    musicd = int(request.args.get('id'))
    user_id = session.get('user_id')
    cursor = conn.cursor()
    sql = "SELECT music_id FROM buy WHERE id = '%s' " % user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    sql = "SELECT free FROM music WHERE music_id = '%s' " % musicd
    cursor.execute(sql)
    results0 = cursor.fetchall()
    print(results0[0])
    for k in results0:
        if 1 == k[0]:
            flash("此歌曲为免费歌曲，无需购买")
            return render_template("home/msg.html")
    for rol in results:
        if musicd == rol[0]:
            flash("您已经购买过此歌曲，请勿重复购买！")
            return render_template("home/msg.html")
    result = User.query.filter(User.id == session.get('user_id')).first()
    uss = result.wallet
    uss = uss - 2
    # print(uss)
    if uss < 0:
        flash("账户余额不足，请充值后再试")
    else:
        sql = "UPDATE user SET wallet = '%s' WHERE id = '%s' " % (uss, user_id)
        cursor.execute(sql)
        conn.commit()
        wallet = uss
        buy = Buy(
            id=session.get('user_id'),
            music_id=musicd
        )
        db.session.add(buy)
        db.session.commit()
        flash("购买成功，账户扣除2元，当前余额%d元" % wallet)
    return render_template("home/msg.html")


# 搜索
@home.route("/search")
def search():
    key = request.args.get('key')
    count = Music.query.filter(
        Music.music_name.ilike('%' + key + '%')
    ).count()

    page_data = Music.query.filter(
        Music.music_name.ilike('%' + key + '%')
    ).order_by(
        Music.listen.desc()
    )
    page_data.key = key
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # cursor = conn.cursor()
    # sql = "SELECT * FROM music WHERE music_name = '%s' " % key
    #
    # cursor.execute(sql)
    # results = cursor.fetchall()
    # print(results)
    return render_template("home/search.html", name=session.get('user'), key=key, count=count, page_data=page_data)
