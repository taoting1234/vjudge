from flask_cors import CORS
from flask_redis import FlaskRedis

from app.api.v1 import bp_v1
from flask import Flask
from app.models.base import db

cors = CORS(supports_credentials=True)
redis = FlaskRedis()


def register_plugin(flask_app):
    # 注册sqlalchemy
    db.init_app(flask_app)

    # 初始化数据库
    with flask_app.app_context():
        db.create_all()

    # 注册cors
    cors.init_app(flask_app)

    # 注册redis
    redis.init_app(flask_app)


def register_blueprint(flask_app):
    flask_app.register_blueprint(bp_v1)


def create_app():
    flask_app = Flask(__name__)

    # 导入配置
    flask_app.config.from_object('app.config.setting')
    flask_app.config.from_object('app.config.secure')

    register_plugin(flask_app)
    register_blueprint(flask_app)

    return flask_app
