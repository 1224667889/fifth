from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os

socketio = SocketIO()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = 'lulubao'#flaskwtf用
    app.config['SECRET_KEY'] = os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除
    # 链接mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % ('root', 'mirror', 'localhost:4036', 'flask_chat')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    global db
    db = SQLAlchemy(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    socketio.init_app(app)
    return app

