from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from app.models import User, Room, Comment
from app import db
import datetime

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
    out_dict = {
        'msg': message['msg'],
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'head': session.get('head', ''),
        'username': session.get('name', '')
    }
    _user = User.query.filter_by(username=session['username']).first()
    _room = Room.query.filter_by(hs=session['room']).first()
    new_comment = Comment(user_id=_user.id, room_id=_room.id, content=message['msg'], addtime=datetime.datetime.now())
    db.session.add(new_comment)
    db.session.commit()
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
