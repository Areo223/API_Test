import json

from flask import request, g

from utils.logs.log import logger


def save_response_log(response):
    """
    保存响应日志
    :param response: 响应对象
    """
    if request.method == "HEAD":
        return
    else:
        logger.info(
            f'【{g.get("request_id")}】【{g.get("user_name")}】【{g.get("user_ip")}】【{request.method}】【{request.full_path}】, '
            f'\n响应数据:{json.loads(response[0])}\n'
       )
        """
        【b0d2bdce-2701-48a3-85a6-9196215a54ca】【管理员】【127.0.0.1】【GET】【/api/api-test/api/list?page_num=1&page_size=20&detail=true&module_id=1&project_id=1,
        响应数据: {'status': 200, 'message': '获取成功', 'data': {'total': 2, 'data': [
            {'id': 1, 'name': 'test', 'project_id': 1, 'module_id': 1, 'addr': 'http://localhost:8023/api-test/api',
             'method': 'GET', 'use_count': 0, 'level': 'P1', 'status': 0, 'create_user': 1},
            {'id': 2, 'name': 'yiyu_login', 'project_id': 1, 'module_id': 1,
             'addr': 'http://localhost:8080/diary/login', 'method': 'POST', 'use_count': 0, 'level': 'P1', 'status': 1,
             'create_user': 1}]}} )
        """

def register_after_hooks(app):
    """
    注册钩子函数
    :param app:
    """
    @app.after_request
    def after_request_save_response_log(response):
        # 在响应头添加 X-Request-Id 字段，作为标识
        response.headers['X-Request-Id'] = str(g.request_id)
        # 设置响应头的 Content-Type 为 application/json
        response.headers['Content-Type'] = 'application/json'
        save_response_log(response.response)
        return response