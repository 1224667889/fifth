import datetime
from app import db

#用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)  #用户名
    name = db.Column(db.String(100))    #昵称
    password = db.Column(db.String(18)) #密码
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now())    #创建时间
    head = db.Column(db.String(100))    #头像地址
    comments = db.relationship('Comment', backref='user')
    collects = db.relationship('Collect', backref='user')
#收藏模型
class Collect(db.Model):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    on = db.Column(db.Boolean, default=False)
#评论模型
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))#创建者
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))#创建位置
    content = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
#房间模型
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))#创建者
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    hs = db.Column(db.String(255))
    head = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    comments = db.relationship('Comment', backref='room')
    collects = db.relationship('Collect', backref='room')
