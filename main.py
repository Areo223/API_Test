# 导入flask_migrate插件
from flask_migrate import Migrate
from sqlalchemy import false

# 导入apps包,运行__init__.py,加载create_app()
from apps import create_app,db
from config import _main_server_port
# 调用create_app()
app = create_app()
if app is None:
    print("创建 app 实例失败，无法输出路由信息。")
else:
    migrate = Migrate(app, db)

if __name__ == '__main__':
    print("所有已注册的路由：")
    for rule in app.url_map.iter_rules():
        print(f"路径: {rule.rule}, 方法: {list(rule.methods)}")
    app.run(host='0.0.0.0', port=_main_server_port, debug=False)
