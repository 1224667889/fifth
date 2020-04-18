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

@main.route('/room/<string:hs>')
@is_login
def room(hs):
    """Chat room. The user's name and room must be stored in
    the session."""
    room = Room.query.filter_by(hs=hs).first()
    inhs = session.get('room', '')
    if room:
        if not inhs:
            return redirect(url_for('.join_room', name=room.name))
        else:
            key = session.get('key', '')
            if key == hs + room.password:
                username = session.get('username', '')
                try:
                    user = User.query.filter_by(username=username).first()
                except:
                    return '用户参数错误'
                if room.user_id == user.id:
                    #管理员
                    print('gly')
                    #return render_template('chat.html', room=room.name, hs=room.hs)
                    return render_template('chat3.html')
                else:
                    #用户
                    #return render_template('chat.html', room=room.name, hs=room.hs)
                    return render_template('chat3.html')
            else:
                return redirect(url_for('.join_room', name=room.name))
    else:
        return "房间不存在"

@main.route('/init', methods=['POST'])
def init():
    username = session.get('username', '')
    #try:
    #    user = User.query.filter_by(name=name).first()
    #except:
    #    return '用户参数错误'
    user = User.query.filter_by(username=username).first()
    user = {
        "head": user.head,
        "name": user.name,
        "status": "online"
    }
    url = request.form.get('url')
    hs = url.split('/')[-1]
    room = Room.query.filter_by(hs=hs).first()
    comments = room.comments
    comments_list = []
    for i in comments:
        new_comment = {
            "head": i.user.head,
            "name": i.user.name,
            "content": i.content,
            "time": i.addtime.strftime('%Y-%m-%d %H:%M:%S')
        }
        comments_list.append(new_comment)
    return {"user": user, "room": room.name, "hs": str(hash(room.name)), "comments": comments_list}

@main.route('/online', methods=['POST'])
def online():
    _user = User.query.filter_by(username=session['username']).first()
    url = request.form.get('url')
    hs = url.split('/')[-1]
    _room = Room.query.filter_by(hs=hs).first()
    for i in _user.collects:
        for j in _room.collects:
            if i == j:
                flag = j.on
                break
    if flag:
        return {"code": 1, "msg": "你不能在同一个房间开两个马甲"}
    else:
        return {"code": 0, "msg": "成功进入房间:" + _room.name}

@main.route('/users', methods=['POST'])
def users():
    url = request.form.get('url')
    hs = url.split('/')[-1]
    room = Room.query.filter_by(hs=hs).first()
    others = room.collects
    otherslist = []
    for i in others:
        if i.on:
            status = "online"
        else:
            status = "offline"
        new_user = {
            "head": i.user.head,
            "name": i.user.name,
            "status": status
        }
        otherslist.append(new_user)
    return {"list": otherslist}

@main.route('/selfinit', methods=['POST'])
def selfinit():
    username = session.get('username', '')
    user = User.query.filter_by(username=username).first()
    rooms = user.collects
    roomslist = []
    for i in rooms:
        new_user = {
            "head": i.room.head,
            "name": i.room.name,
            "status": "online"
        }
        roomslist.append(new_user)
    return {"list": roomslist}

@main.route('/create/in', methods=['POST'])
@is_login
def create_in():
    username = request.form.get('username')
    password = request.form.get('password')
    room = Room.query.filter_by(name=username).first()
    if room:
        return {"code": 1, "message": "房间名已被占用！", "html": "/create"}
    else:
        #不存在就新建
        try:
            # 生成并添加房间数据
            user = User.query.filter_by(username=session['username']).first()
            hs = str(hash(username))
            new_room = Room(name=username, password=password, user_id=user.id, hs=hs)
            db.session.add(new_room)
            db.session.commit()
            session['room'] = hs
            session['key'] = hs + password
            return {"code": 0, "message": "创建成功!", "html": "/room/" + hs}
        except Exception as e:
            print(e)
            db.session.rollback()
            return '生成错误'

@main.route('/join/in', methods=['POST'])
@is_login
def join_in():
    username = request.form.get('username')
    password = request.form.get('password')
    room = Room.query.filter_by(name=username).first()
    if room:
        if password == room.password:
            hs = str(hash(username))
            session['key'] = hs + password
            session['room'] = hs
            user = User.query.filter_by(username=session['username']).first()
            id = user.id
            others = room.collects
            for i in others:
                if i.user.id == id:
                    return {"code": 0, "message": "进入房间中！", "hs": hs}
            new_collect = Collect(user_id=id, room_id=room.id)
            db.session.add(new_collect)
            db.session.commit()
            return {"code": 0, "message": "进入房间中！", "hs": hs}
        else:
            return {"code": 1, "message": "密码错误!"}
    else:
        return {"code": 1, "message": "房间不存在！"}

@main.route('/login/in', methods=['POST'])
@isnot_login
def login_in():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        if password == user.password:
            session['username'] = username
            session['name'] = user.name
            session['head'] = user.head
            return {"code": 0, "message": "登录成功!"}
        else:
            return {"code": 1, "message": "密码错误!"}
    else:
        return {"code": 1, "message": "用户不存在!"}

@main.route('/register/in', methods=['POST'])
@isnot_login
def register_in():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return {"code": 1, "message": "账号已存在!"}
    else:
        try:
            # 生成并添加用户数据
            new_user = User(username=username, name=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            session['name'] = username
            return {"code": 0, "message": "注册成功!"}
        except Exception as e:
            print(e)
            db.session.rollback()