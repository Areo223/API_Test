import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 导入第三方插件
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate

# 初始化
db = SQLAlchemy()
migrate = Migrate()

# 与app对象建立绑定
def init_exts(app):
    db.init_app(app)
    migrate.init_app(app, db)

