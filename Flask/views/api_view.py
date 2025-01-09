from flask import request, json, jsonify

from Flask.blueprint import api_test
from Flask.exts import db
from Flask.models import api


@api_test.route('/hello')
def hello_world():
    return 'Hello World!'

# 新增api接口
@api_test.route('/api', methods=['POST'])
def api_add():
    try:
        data = json.loads(request.get_data())
        a = api.Api(api_name=data['api_name'], method= data['method'], url=data['url'], parametrize=data['parametrize'], json=data['json'], expect=data['expect'], description=data['description'])
        db.session.add(a)
        db.session.commit()
        return 'api_add'
    except Exception as e:
        # 记录异常信息
        print(f"An error occurred: {e}")
        # 回滚数据库会话
        db.session.rollback()
        # 返回错误信息给客户端
        return jsonify({'error': 'Failed to add API'}), 500



# 查询api接口
@api_test.route('/api',methods=['GET'])
def api_list():
    return 'api_list'

# 删除api接口
@api_test.route('/api',methods=['DELETE'])
def api_delete():
    return 'api_delete'

# 更新api接口
@api_test.route('/api',methods=['PUT'])
def api_update():
    return 'api_update'