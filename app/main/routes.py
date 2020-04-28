from flask import session, redirect, url_for, render_template, request
import functools
from . import main
from app.models import User, Room, Collect
from app import db
from .re_test import re_password, re_username
import random, string, base64

def random_name(perfix,length=16):
    # 生成a-z 0-9 A-Z
    str = string.ascii_letters + string.digits
    return ''.join(random.sample(str, length))+'.'+perfix


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

@main.route('/headupload',methods=['POST'])
@is_login
def headupload():
    file = request.form['image']
    file = file.replace("data:image/png;base64,", "")

    img = base64.b64decode(file)

    filename = 'static/upload/' + random_name("png")
    fh = open("app/" + filename, "wb")
    fh.write(img)
    fh.close()
    try:
        username = session.get('username', '')
        user = User.query.filter_by(username=username).first()
        user.head = filename
        db.session.commit()
        return {"code": 0, "result": "修改成功", "file": filename}
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"code": 1, "result": "修改失败"}


@main.route('/change', methods=['POST'])
@is_login
def change():
    username = session.get('username', '')
    user = User.query.filter_by(username=username).first()
    if user:
        password0 = request.form.get("password0")#p0原密码
        password = request.form.get("password")#p新密码
        password2 = request.form.get("password2")#p2确认密码
        if user.password == password0:
            if password == password2:
                if re_password(password):
                    if password == user.password:
                        return {"code": 1, "msg": "新旧密码一致"}
                    else:
                        user.password = password
                        db.session.commit()
                        return {"code": 0, "msg": "修改密码成功"}
                else:
                    return {"code": 1, "msg": "新密码格式出错(6-18位,不能使用纯数字!)"}
            else:
                return {"code": 1, "msg": "两次密码不一致"}
        else:
            return {"code": 1, "msg": "原密码错误"}
    else:
        return {"code": 1, "msg": "用户不存在"}

@main.route('/changedata',methods=['POST'])
@is_login
def changedata():
    username = session.get('username', '')
    user = User.query.filter_by(username=username).first()
    if user:
        try:
            user.name = request.form.get("name")
            db.session.commit()
            print(user.name)
            session['name'] = user.name
            return {"code": 0, "msg": "修改成功"}
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"code": 1, "msg": "无法进行修改"}
    else:
        return {"code": 1, "msg": "用户错误"}

@main.route('/room/<string:hs>')
@is_login
def room(hs):
    """Chat room. The user's name and room must be stored in
    the session."""
    room = Room.query.filter_by(hs=hs).first()
    inhs = session.get('room', '')
    if room:
        if not inhs:
            return redirect(url_for('.join_room', name=room.hs))
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
                    return render_template('chat4.html')
                else:
                    #用户
                    #return render_template('chat.html', room=room.name, hs=room.hs)
                    return render_template('chat3.html')
            else:
                return redirect(url_for('.join_room', name=room.name))
    else:
        return "房间不存在"

@main.route('/init', methods=['POST'])
@is_login
def init():
    try:
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
        return {"code": 0, "msg": "获取成功", "user": user, "room": room.name, "hs": room.hs, "comments": comments_list, "head": room.head}
    except Exception as e:
        print(e)
        return {"code": 1, "msg": "获取失败"}

@main.route('/online', methods=['POST'])
@is_login
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
@is_login
def users():
    url = request.form.get('url')
    hs = url.split('/')[-1]
    room = Room.query.filter_by(hs=hs).first()
    others = room.collects
    otherslist = []
    l_in = 0
    l_out = 0
    for i in others:
        if i.on:
            status = "online"
            l_in += 1
        else:
            status = "offline"
        l_out += 1
        new_user = {
            "head": i.user.head,
            "name": i.user.name,
            "status": status
        }
        otherslist.append(new_user)
    return {"list": otherslist, "l_in": l_in, "l_out": l_out}

@main.route('/me', methods=['POST'])
@is_login
def user():
    username = session.get('username', '')
    user = User.query.filter_by(username=username).first()
    return {"username": user.username, "name": user.name, "head": user.head}

@main.route('/other', methods=['POST'])
def otr():
    #username = session.get('username', '')
    id = request.form.get("id")
    id = id.split('/')[-1]
    user = User.query.filter_by(id=id).first()
    return {"username": user.username, "name": user.name, "head": user.head}

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
            "hs": i.room.hs,
            "status": "online"
        }
        roomslist.append(new_user)
    return {"list": roomslist}

@main.route('/create/in', methods=['POST'])
@is_login
def create_in():
    username = request.form.get('username')
    password = request.form.get('password')
    hs = hash(username)
    while True:
        room = Room.query.filter_by(hs=hs).first()
        if room:
            hs += 1
        else:
            break
    hs =str(hs)
    #不存在就新建
    try:
        # 生成并添加房间数据
        user = User.query.filter_by(username=session['username']).first()
        new_room = Room(name=username, password=password, user_id=user.id, hs=hs, head="static/upload/room.gif")
        db.session.add(new_room)
        db.session.commit()
        collect = Collect(user_id=user.id, room_id=new_room.id)
        db.session.add(collect)
        db.session.commit()
        session['room'] = hs
        session['key'] = hs + password
        return {"code": 0, "message": "创建成功!", "html": "/room/" + hs}
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"code": 1, "message": '生成错误'}

@main.route('/join/in', methods=['POST'])
@is_login
def join_in():
    hs = request.form.get('username')
    password = request.form.get('password')
    room = Room.query.filter_by(hs=hs).first()
    if room:
        if password == room.password:
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

@main.route('/loginout')
@is_login
def loginout():
    session.clear()
    return redirect('/')

@main.route('/register/in', methods=['POST'])
@isnot_login
def register_in():
    username = request.form.get('username')
    password = request.form.get('password')
    if re_username(username) and re_password(password):
        user = User.query.filter_by(username=username).first()
        if user:
            return {"code": 1, "message": "账号已存在!"}
        else:
            try:
                # 生成并添加用户数据
                new_user = User(username=username, name=username, password=password, head="static/upload/index.png")
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                session['name'] = username
                return {"code": 0, "message": "注册成功!"}
            except Exception as e:
                print(e)
                db.session.rollback()
    else:
        return {"code": 1, "message": "账号或密码格式错误!"}