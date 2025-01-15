# 导入flask_migrate插件
from flask_migrate import Migrate
# 导入apps包,运行__init__.py,加载create_app()
from apps import create_app,db
from config import _main_server_port
# 调用create_app()
app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_main_server_port, debug=False)