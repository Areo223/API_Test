from flask import Blueprint
from . import models

# 蓝图
blue = Blueprint('user', __name__)


@blue.route('/')
def index():
    from. import exts
    return 'index'


@blue.route('/add')
def add():
    from. import exts
    from models.user import User
    # 添加一条数据
    u = User()
    u.name = 'admin'
    u.email = '1234@123'
    u.password = '1234'

    exts.db.session.add(u)
    exts.db.session.commit()

    # 同时添加多条数据
    users = []
    for i in range(1, 6):
        u = User()
        u.name = 'admin' + str(i)
        u.email = '<EMAIL>' + str(i)
        u.password = '<PASSWORD>' + str(i)
        users.append(u)

    try:
        exts.db.session.add_all(users)
        exts.db.session.commit()
    except Exception as e:
        exts.db.session.rollback()  # 回滚
        exts.db.session.flush()  # 清空缓存
        return str(e)
    return 'ok'


@blue.route('/delete')
def delete():
    from. import exts
    from models.user import User
    u = User.query.first()  # 查询第一条数据

    exts.db.session.delete(u)
    exts.db.session.commit()

    return 'ok'


@blue.route('/update')
def update():
    from. import exts
    from models.user import User
    u = User.query.first()

    u.name = 'update'
    u.email = '<EMAIL>'
    u.password = '<PASSWORD>'

    exts.db.session.add(u)
    exts.db.session.commit()

    return 'ok'


@blue.route('/query')
def query():
    from. import exts
    from models.user import User
    u = User.query.first()
    return str(u) if u else 'no user found'