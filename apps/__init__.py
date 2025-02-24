from flask import Flask

from apps.base_model import db
from apps.base_view import Blueprint
from apps.hooks.after_request import register_after_hooks
from apps.hooks.before_request import register_before_hooks
from apps.hooks.error_handler import register_errorhandler_hooks
from config import _SystemConfig
from utils.util.json_util import CustomEncoder
from utils.view import restful


def create_app():
    try:
        # 创建Flask应用
        app = Flask(__name__)
        # 注册自定义JSON编码器
        app.json_encoder = CustomEncoder
        # 加载配置
        app.config.from_object(_SystemConfig)
        # 将db对象绑定到app对象上
        app.db=db
        # 将restful对象绑定到app对象上
        app.restful = restful
        # 注册数据库
        db.init_app(app)
        db.app = app

        # 注册钩子函数
        register_before_hooks(app)
        register_after_hooks(app)
        register_errorhandler_hooks(app)

        # 创建蓝图实例
        bp = Blueprint('example', __name__)

        @bp.login_get('/test')
        def test():
            return 'Test route'

        # 注册蓝图
        from apps.api_test.blueprint import api_test
        from apps.system.blueprint import system

        #将蓝图注册到app
        app.register_blueprint(bp)
        app.register_blueprint(api_test)
        app.register_blueprint(system)

        # 加载模型
        from apps.api_test import model_factory
        from apps.system import model_factory

        from .base_view import url_required_map
        app.url_required_map = url_required_map


        return app
    except Exception as e:
        print(f"app实例化出现错误:{e}")