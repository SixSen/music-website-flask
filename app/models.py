# _*_ coding: utf-8 _*_
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

'''
models文件是有关数据库相关文件
'''

app = Flask(__name__)

# 用于连接数据的数据库。
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:1232123@127.0.0.1:3306/musicdb"
# Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)  # 编号
    name = db.Column(db.String(100), nullable=False)  # 昵称
    pwd = db.Column(db.String(100), nullable=False)  # 密码
    email = db.Column(db.String(100), nullable=False)  # 邮箱
    vclass = db.Column(db.Integer, default=0, nullable=False)  # 会员标志
    phone = db.Column(db.String(11), nullable=False)  # 手机号
    end = db.Column(db.DateTime, index=True, default=datetime.datetime.now())  # 会员到期日期
    wallet = db.Column(db.Float, default=0, nullable=False)  # 余额

    # music = db.relationship('Music', backref='music')
    # music = db.relationship('Music', secondary=library)
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

    def get_vclass(self):
        return self.vclass
    # user = db.relationship('Library')
    # def __repr__(self):
    #     return '<User %r>' % self.name


class Music(db.Model):
    __tablename__ = 'music'
    music_id = db.Column(db.Integer, primary_key=True, unique=True)  # 歌曲编号
    music_name = db.Column(db.String(100), nullable=False)  # 歌名
    author = db.Column(db.String(100), nullable=True)  # 歌手名
    download = db.Column(db.Integer, default=0, nullable=False)  # 下载次数
    listen = db.Column(db.Integer, default=0, nullable=False)  # 播放次数
    style = db.Column(db.String(50), nullable=True)  # 歌曲风格
    free = db.Column(db.Integer, nullable=False)  # 是否免费
    address = db.Column(db.String(100), nullable=True)  # 歌曲地址

    # music = db.relationship('Library', backref="music")

    # def __repr__(self):
    #     return '<User %r>' % self.name


# library = db.Table('library',
#         db.Column('id', db.Integer, db.ForeignKey('user.id')),
#         db.Column('list_id', db.Integer, db.ForeignKey('music.music_id'))
#         )
#


class Library(db.Model):
    __tablename__ = 'library'
    library_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # library主键
    id = db.Column(db.Integer, nullable=False)  # 收藏用户id
    music_id = db.Column(db.Integer, nullable=False)  # 收藏歌单id

    # librarys = db.relationship('')

    # def __repr__(self):
    #     return '<User %r>' % self.name


class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # 收藏歌单id
    music_id = db.Column(db.Integer, nullable=False)  # 歌曲id

    # list = db.relationship('Library')

    # def __repr__(self):
    #     return '<User %r>' % self.name


class Buy(db.Model):
    __tablename__ = 'buy'
    buy_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # 购买id
    id = db.Column(db.Integer, nullable=False)  # 购买歌曲用户id
    music_id = db.Column(db.Integer, nullable=False)  # 已购买歌曲id


#  buy = db.relationship('User')
# def __repr__(self):
#     return '<User %r>' % self.name


class Board(db.Model):
    __tablename__ = 'board'
    board_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    music_id = db.Column(db.Integer, nullable=False)
    # music_name = db.Column(db.String(100), nullable=False)
    # music_names = db.relationship("music", backref='board')


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(10), primary_key=True, nullable=False, unique=True)  # 管理员账号
    admin_pwd = db.Column(db.String(100), nullable=False)  # 管理员密码

    # def __repr__(self):
    #     return '<User %r>' % self.name


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # 歌手id
    author_name = db.Column(db.String(100), nullable=False)  # 歌手名

    # def __repr__(self):
    #     return '<User %r>' % self.name


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
