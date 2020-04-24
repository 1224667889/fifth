from flask import session
from flask_socketio import emit, join_room, leave_room, close_room
from .. import socketio
from app.models import User, Room, Comment
from app import db
import datetime
import os,random,string,base64

def random_name(perfix,length=16):
    # 生成a-z 0-9 A-Z
    str = string.ascii_letters + string.digits
    return ''.join(random.sample(str, length))+'.'+perfix

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    url = message["msg"]
    room = url.split('/')[-1]
    join_room(room)
    out_dict = {
        'msg': '进入了房间',
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'head': session.get('head', ''),
        'username': session.get('name', '')
    }
    msg = {
        "code": 0,
        "msg": out_dict
    }
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=session['room']).first()
    for i in _user.collects:
        for j in _room.collects:
            if i == j:
                j.on = True
                db.session.commit()
                break
    emit('status', msg, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    print(room)
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=room).first()
    new_comment = Comment(user_id=_user.id, room_id=_room.id, content=message['msg'], addtime=datetime.datetime.now())
    db.session.add(new_comment)
    db.session.commit()
    out_dict = {
        'msg': message['msg'],
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'head': _user.head,
        'username': _user.name
    }
    emit('message', out_dict, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    url = message["msg"]
    room = url.split('/')[-1]
    leave_room(room)
    out_dict = {
        'msg': '离开了房间',
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'head': session.get('head', ''),
        'username': session.get('name', '')
    }
    msg = {
        "code": 0,
        "msg": out_dict
    }
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=session['room']).first()
    for i in _user.collects:
        for j in _room.collects:
            if i == j:
                j.on = False
                db.session.commit()
                break
    emit('status', msg, room=room)

@socketio.on('delete', namespace='/chat')
def delete(message):
    url = message["msg"]
    room = url.split('/')[-1]
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=room).first()
    if _user.id == _room.user_id:
        try:
            for like in _room.comments:
                db.session.delete(like)
            for collect in _room.collects:
                db.session.delete(collect)
            db.session.delete(_room)
            db.session.commit()
            msg = {"code": 0, "msg": "删除成功"}
        except Exception as e:
            print(e)
            db.session.rollback()
            msg = {"code": 1, "msg": "未能删除"}
    else:
        msg = {"code": 1, "msg": "你不是管理员"}
    emit('delete', msg, room=room)
    close_room(room)

@socketio.on('name', namespace='/chat')
def name(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    name = message["msg"]
    print(room)
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=room).first()
    if _user.id == _room.user_id:
        try:
            _room.name = name
            db.session.commit()
            msg = {"code": 0, "msg": "管理员修改了房间名称", "name": name}
        except Exception as e:
            print(e)
            db.session.rollback()
            msg = {"code": 1, "msg": "管理员想要修改房间名称，但是失败了"}
    else:
        msg = {"code": 1, "msg": "你不是管理员"}
    emit('name', msg, room=room)

@socketio.on('head', namespace='/chat')
def name(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    file = message["pic"]
    print(room)
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=room).first()
    if _user.id == _room.user_id:
        try:

            file = file.replace("data:image/png;base64,", "")

            img = base64.b64decode(file)

            filename = 'static/upload/' + random_name("png")
            fh = open("app/" + filename, "wb")
            fh.write(img)
            fh.close()

            _room.head = filename
            db.session.commit()

            msg = {"code": 0, "msg": "管理员修改了房间头像", "head": filename}
        except Exception as e:
            print(e)
            db.session.rollback()
            msg = {"code": 1, "msg": "管理员想要修改房间头像，但是失败了"}
    else:
        msg = {"code": 1, "msg": "你不是管理员"}
    emit('head', msg, room=room)