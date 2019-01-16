# 从模块的初始化文件中导入蓝图。
from flask import Blueprint, render_template, redirect, flash, url_for, session, request, Response, abort
from . import admin
from app.models import User, Music, Board, Buy, db, Library, Admin, Author
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, AuthorForm

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


@admin.route("/all/")
def all():
    if not "admin_id" in session:
        return abort(403)
    form = User.query.all()
    # print(form)
    admin_id = session.get("admin_id")
    return render_template("admin/all.html", id=admin_id ,form = form)

@admin.route("/deuser/")
def deuser():
    if not "admin_id" in session:
        return abort(403)
    uid = int(request.args.get("id"))
    form = User.query.all()
    admin_id = session.get("admin_id")
    user = User.query.filter(User.id==uid).first()
    # print(musicd)
    user.vclass = -1
    db.session.add(user)
    db.session.commit()
    flash("已经成功注销id为%d的用户" % uid, "ok")
    return redirect(url_for('admin.all'))



# 删除歌曲
@admin.route('/delete_music/<music_id>')
def delete_music(music_id):
    music = Music.query.get(music_id)
    musicna = music.music_name
    if music:
        try:
            db.session.delete(music)
            db.session.commit()
        except Exception as e:
            print (e)
            flash('删除歌曲失败')
            db.session.rollback()
    else:
        flash('歌曲找不到')
    flash("删除成功歌曲%s" % musicna)
    return redirect(url_for('admin.manage'))


@admin.route('/manage/', methods=['GET', 'POST'])
def manage():
    if not "admin_id" in session:
        return abort(403)
    # 创建自定义的表单类
    author_form = AuthorForm()
    # 验证函数
    if author_form.validate_on_submit():
        # 验证通过获取数据
        author_name = author_form.author.data
        music_name = author_form.music.data
        # 判断歌手是否存在
        author = Author.query.filter_by(author_name=author_name).all()
        # 如果歌手存在
        if author:
            # 判断歌曲是否存在，没有重复歌曲就添加，如果重复就提示错误
            music = Music.query.filter_by(music_name=music_name).all()
            # 如果重复就提示错误
            if music:
                flash('已存在')
            # 没有重复歌曲就添加歌曲
            else:
                try:
                    new_music = Music(music_name=music_name, author=author_name, style=author_form.style.data, free=author_form.free.data, address=author_form.address.data)
                    db.session.add(new_music)
                    db.session.commit()
                    flash("添加成功")
                except Exception as e:
                    print (e)
                    flash('添加歌曲失败')
                    db.session.rollback()
        else:
            # 如果歌手不存在，添加歌手和歌曲
            try:
                new_author = Author(author_name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_music = Music(music_name=music_name, author=author_name, style=author_form.style.data,  free=author_form.free.data, address=author_form.address.data)
                db.session.add(new_music)
                db.session.commit()
                flash("添加成功")
            except Exception as e:
                print (e)
                flash('添加歌手和歌曲失败')
                db.session.rollback()
    else:
        if request.method == 'POST':
            flash('参数不全')

    authors = Author.query.all()
    musics = Music.query.all()
    return render_template('admin/index.html', author=authors, music=musics, form=author_form)