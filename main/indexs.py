from flask import session, redirect, url_for, render_template, request
import functools
from . import main
from app.models import User, Room, Collect
from app import db


def is_login(func):
    # 修饰器 在原修饰器下加 @is_login 若无登录，则跳转至登录
    @functools.wraps(func)
    def inner(*args, **kwargs):
        user = session.get('username')
        if not user:
            return redirect(url_for("main.login"))
        return func(*args, **kwargs)
    return inner
def isnot_login(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        user = session.get('username')
        if user:
            return "无法重复登录"
        return func(*args, **kwargs)
    return inner


@main.route('/', methods=['GET', 'POST'])
def index():
    #session['username'] = 'mirrorlied'
    #session['name'] = 'mirrorlied'
    #return render_template('chat2.html')
    return render_template('index.html')
'''
@main.route('/a', methods=['GET', 'POST'])
def tindex():
    db.drop_all()
    db.create_all()
    new_user = User(username='mirrorlied', name='mirrorlied', password='aaaaaa', head="static/files/2022.jpg")
    db.session.add(new_user)
    db.session.commit()
    new_room = Room(name='room', password='aaa', user_id=1, hs=str(hash('room')), head="static/files/2022.jpg")
    new_room2 = Room(name='room2', password='aaaa', user_id=1, hs=str(hash('room2')), head="static/files/2022.jpg")
    db.session.add(new_room)
    db.session.add(new_room2)
    db.session.commit()
    collect1 = Collect(user_id=1, room_id=1)
    collect2 = Collect(user_id=1, room_id=2)
    db.session.add(collect1)
    db.session.add(collect2)
    db.session.commit()
    session['username'] = 'mirrorlied'
    session['name'] = 'mirrorlied'
    session['head'] = 'static/files/2022.jpg'
    return '初始化成功'
'''
@main.route('/self', methods=['GET', 'POST'])
@is_login
def who():
    return render_template('self.html')
@main.route('/user/<id>', methods=['GET', 'POST'])
def other(id):
    return render_template('user.html')
    #return render_template('self.html')
@main.route('/create')
@is_login
def create():
    return render_template('create.html')
@main.route('/join')
@is_login
def join():
    return render_template('join.html', name="")
@main.route('/joinroom/<string:name>')
@is_login
def join_room(name):
    return render_template('join.html', name=name)
@main.route('/login')
@isnot_login
def login():
    return render_template('login.html')
@main.route('/register')
@isnot_login
def register():
    return render_template('register.html')