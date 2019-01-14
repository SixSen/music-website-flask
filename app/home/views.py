from flask import render_template, redirect, flash, url_for, session, request
from werkzeug.security import generate_password_hash
from . import home
from app.home.forms import LoginForm, RegisterForm, UserdetailForm, PwdForm, WalletForm
from app.models import User, Music, Board, Buy, db, Library
# from app import db, app, rd
import pymysql
import datetime

'''
views是主要的路由文件
'''


# pymysql的数据库连接
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')

# @ home = Blueprint("home",__name__)


# 根路由
@home.route("/")
def index():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/index.html", page_data=page_data)


# 欢迎主页
@home.route("/welcome/")
def welcome():
    page_data = Board.query.filter(
    ).order_by(
        Board.board_id
    )
    return render_template("home/welcome.html", name=session.get('user'), vclass=session.get('vclass'),
                           page_data=page_data)


# 音乐库
@home.route("/fav/")
def fav():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
    cursor = conn.cursor()
    sql = "SELECT music_id FROM library WHERE id = '%s' " % session.get("user_id")
    cursor.execute(sql)
    results = cursor.fetchall()
    musicd = []
    for rol in results:
        musicd.append(rol[0])
    page_data = []
    for fid in musicd:
        data = Music.query.filter(
            Music.music_id == fid
        ).order_by(
            Music.listen.desc()
        )
        # print(fid)
        page_data += data
    # print(page_data)
    page_data.reverse()
    return render_template("home/fav.html", name=session.get('user'), page_data=page_data)


@home.route("/mybuy/")
def mybuy():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
    cursor = conn.cursor()
    sql = "SELECT music_id FROM buy WHERE id = '%s' " % session.get("user_id")
    cursor.execute(sql)
    results = cursor.fetchall()
    musicd = []
    for rol in results:
        musicd.append(rol[0])
    page_data = []
    for bid in musicd:
        data = Music.query.filter(
            Music.music_id == bid
        ).order_by(
            Music.listen.desc()
        )
        # print(bid)
        page_data += data
    # print(page_data)
    page_data.reverse()
    return render_template("home/mybuy.html", name=session.get('user'), page_data=page_data)


@home.route("/pop/")
def pop():
    page_data = Music.query.filter(
        Music.style == 'Pop'
    ).order_by(
        Music.listen.desc()
    ).limit(10)
    return render_template("home/pop.html", name=session.get('user'), page_data=page_data)


@home.route("/jazz/")
def jazz():
    page_data = Music.query.filter(
        Music.style == 'Jazz'
    ).order_by(
        Music.listen.desc()
    ).limit(10)
    return render_template("home/jazz.html", name=session.get('user'), page_data=page_data)


@home.route("/rb/")
def rb():
    page_data = Music.query.filter(
        Music.style == 'R&B'
    ).order_by(
        Music.listen.desc()
    ).limit(10)
    return render_template("home/rb.html", name=session.get('user'), page_data=page_data)


@home.route("/cla/")
def cla():
    page_data = Music.query.filter(
        Music.style == 'classical'
    ).order_by(
        Music.listen.desc()
    ).limit(10)
    return render_template("home/cla.html", name=session.get('user'), page_data=page_data)


@home.route("/folk/")
def folk():
    page_data = Music.query.filter(
        Music.style == 'Folk'
    ).order_by(
        Music.listen.desc()
    ).limit(10)
    return render_template("home/folk.html", name=session.get('user'), page_data=page_data)


# 登录
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if not user.check_pwd(data["pwd"]):  # 密码采用pbkdf2:sha256方式加密-所以要用这种方案判断密码
                flash("密码错误！", "err")
                return redirect(url_for("home.login"))
        else:
            flash("账户不存在！", "err")
            return redirect(url_for("home.login"))

        vclass = user.get_vclass()
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
    return redirect(url_for('home.login'))


@home.route("/out/")
def out():
    flash("您已成功登出！", "ok")
    return redirect(url_for('home.logout'))


# 个人中心——修改个人资料
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


# 个人中心——密码修改
@home.route("/pwd/", methods=["GET", "POST"])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user1 = User.query.filter_by(name=session["user"]).first()
        if not user1.check_pwd(data["old_pwd"]):
            flash("旧密码错误！", "err")
            return redirect(url_for('home.pwd'))
        user1.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user1)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html", name=session.get('user'), form=form)


# 个人中心——订阅会员
@home.route("/sub/", methods=["GET", "POST"])
def sub():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user2 = User.query.filter_by(name=session["user"]).first()
        if not user2.check_pwd(data["old_pwd"]):
            flash("旧密码错误！", "err")
            return redirect(url_for('home.pwd'))
        user2.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user2)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout'))
    return render_template("home/subscribe.html", name=session.get('user'), form=form)


# 个人中心——确认订阅
@home.route("/getsub/")
def getsub():
    user3 = User.query.filter_by(name=session["user"]).first()
    if user3.vclass == 1:
        flash("您已经是会员了，无需订购", "err")
        return redirect(url_for('home.sub'))
    else:
        uss = user3.wallet
        uss = uss - 15
        if uss < 0:
            flash("余额不足，余额需要大于15元才可办理", "err")
            return redirect(url_for('home.sub'))
        user3.wallet = uss
        user3.vclass = 1
        next_end = datetime.datetime.now() + datetime.timedelta(days=30)
        user3.end = next_end
        db.session.add(user3)
        db.session.commit()
        end = user3.end.strftime('%Y-%m-%d')
        flash("您已经成功办理会员，当前余额%d元，会员有效期至%s" % (uss, end), "ok")
        session.pop("vclass", None)
        session["vclass"] = 1
        return redirect(url_for('home.sub'))


# 个人中心——充值钱包
@home.route("/wallet/", methods=["GET", "POST"])
def wallet():
    userm = User.query.filter_by(name=session["user"]).first()
    form = WalletForm()
    if form.validate_on_submit():
        data = form.data
        money = float(data["money"])
        if money <= 0:
            flash("充值金额需大于0！", "err")
            return redirect(url_for('home.wallet'))
        else:
            uss = userm.wallet
            uss = uss + money
            userm.wallet = uss
            db.session.add(userm)
            db.session.commit()
            flash("充值成功！，当前账户余额为%.2f元" % uss, "ok")
            return redirect(url_for('home.wallet'))
    return render_template("home/wallet.html", name=session.get('user'), form=form, money=userm.wallet)


# 播放音乐
@home.route("/play/")
def play():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
    if session.get('user') is None:
        flash("请先登录才能播放音乐", "err")
        return redirect(url_for('home.login'))
    cursor = conn.cursor()
    musicid = int(request.args.get('id'))
    vclass = session.get('vclass')
    isbuy = 0
    sql = "SELECT free FROM music WHERE music_id = '%s' " % musicid
    cursor.execute(sql)
    results0 = cursor.fetchall()
    for k in results0:
        if 1 == k[0]:
            isbuy = 1
    if vclass == 0:
        id = session.get('user_id')
        sql = "SELECT music_id FROM buy WHERE id = '%s' " % id
        cursor.execute(sql)
        results = cursor.fetchall()
        for rol in results:
            if musicid == rol[0]:
                isbuy = 1
        if isbuy == 1:
            music = Music.query.filter(
                Music.music_id == musicid
            ).first()
            add = music.address
            pla = music.listen
            # print(pla)
            pla = pla + 1
            music.listen = pla
            # print(music.listen)
            db.session.add(music)
            db.session.commit()
            return render_template("home/play.html", name=session.get('user'), user=session.get('user_id'), id=musicid,
                                   add=add)
        else:
            flash('请先购买此歌曲或订阅会员-err:%d' % musicid)
            return render_template("home/msg.html", name=session.get('user'))
    else:
        music = Music.query.filter(
            Music.music_id == musicid
        ).first()
        add = music.address
        pla = music.listen
        # print(pla)
        pla = pla + 1
        music.listen = pla
        # print(music.listen)
        db.session.add(music)
        db.session.commit()
        return render_template("home/play.html", name=session.get('user'), user=session.get('user_id'), id=musicid,
                               add=add, music_name=music.music_name)


# 下载音乐
@home.route("/download/")
def download():
    musicid = int(request.args.get('id'))
    music = Music.query.filter(Music.music_id == musicid).first()
    dow = music.download
    # print(pla)
    dow = dow + 1
    music.download = dow
    # print(music.listen)
    db.session.add(music)
    db.session.commit()
    link = "开始下载歌曲： %s" % music.music_name
    return link


# 注册
@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        new_user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("注册成功！", "ok")
    return render_template("home/register.html", form=form)


# 收藏音乐
@home.route("/like/")
def like():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
    musicd = int(request.args.get('id'))
    # print(musicd)
    user_id = session.get('user_id')
    cursor = conn.cursor()
    sql = "SELECT music_id FROM library WHERE id = '%s' " % user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    for rol in results:
        if musicd == rol[0]:
            flash("您已经收藏过此歌曲o(∩_∩)o")
            return render_template("home/msg.html", name=session.get('user'))
    library = Library(
        id=session.get('user_id'),
        music_id=musicd
    )
    db.session.add(library)
    db.session.commit()
    flash("收藏成功！已经添加到“我喜欢的音乐”当中")
    return render_template("home/msg.html", name=session.get('user'))


# 取消收藏
@home.route("/del_like/")
def del_like():
    musicd = int(request.args.get('id'))
    library = Library.query.filter(Library.id == session.get('user_id'), Library.music_id == musicd).first()
    # print(musicd)
    db.session.delete(library)
    db.session.commit()
    flash("已经取消收藏啦 :-D", "ok")
    return redirect(url_for('home.fav'))


# 购买
@home.route("/buy")
def buy():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1232123', db='musicdb')
    # conn = pymysql.connect(host='39.106.214.230', port=3306, user='root', passwd='nucoj', db='musicdb')
    musicd = int(request.args.get('id'))
    user_id = session.get('user_id')
    cursor = conn.cursor()
    sql = "SELECT music_id FROM buy WHERE id = '%s' " % user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    sql = "SELECT free FROM music WHERE music_id = '%s' " % musicd
    cursor.execute(sql)
    results0 = cursor.fetchall()
    for k in results0:
        if 1 == k[0]:
            flash("此歌曲为免费歌曲，无需购买")
            return render_template("home/msg.html", name=session.get('user'))
    if int(session.get("vclass")) == 1:
        flash("您现在为会员，无需单独购买歌曲")
        return render_template("home/msg.html", name=session.get('user'))
    for rol in results:
        if musicd == rol[0]:
            flash("您已经购买过此歌曲，请勿重复购买！")
            return render_template("home/msg.html", name=session.get('user'))
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
    return render_template("home/msg.html", name=session.get('user'))


# 搜索
@home.route("/search")
def search():
    key = request.args.get('key')
    # kee为防止SQL注入设置的过滤用字符串
    kee = key.replace('%', '`')
    if kee != key:
        key = ""

    if key == "":
        return redirect(url_for('home.welcome'))

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
