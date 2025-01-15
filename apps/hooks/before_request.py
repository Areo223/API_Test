import uuid

from flask import g, request

from utils.logs.log import logger
from utils.view.required import check_login_and_permissions


def register_before_hooks(app):
    @app.before_request
    def set_user_info():
        """
          第一个执行
          在每个请求之前设置用户信息。
          初始化 g.user_id, g.user_name, g.api_permissions, g.business_list 为 None 或空列表。
          在第四个钩子函数中填充
          """
        g.user_id,g.user_name,g.api_permission,g.business_list = None,None,[],[]

    @app.before_request
    def parse_request():
        """
        第二个执行
        解析请求。
        从请求中获取用户信息，并将其设置到 g.user_id 和 g.user_name 中。
        """
        g.user_id = 1
        g.user_name = "admin"

    @app.before_request
    def set_request_id():
        """
        第二个执行
        设置请求 ID。
        从请求中获取用户信息，并将其设置到 g.user_id 和 g.user_name 中。
        """
        g.request_id = uuid.uuid4()

    @app.before_request
    def parse_request_ip():
        """
        第三个执行
        在每个请求之前解析请求的IP地址。
        从请求头中获取 X-Forwarded-History 或 X-Forwarded-From，如果不存在，则使用 request.remote_addr。
        其中 X-Forwarded-History 用于记录请求的历史IP地址，X-Forwarded-From 用于记录请求的原始IP地址。
        request.remote_addr 是 Flask 提供的属性，用于获取客户端的IP地址,但是这通常是代理服务器的IP地址。
        """
        g.user_ip = request.headers.get("X-Forwarded-History", request.headers.get("X-Forwarded-From", request.remote_addr))
    @app.before_request
    def login_and_pemission():
        """
        第四个执行
        在每个请求之前进行登录校验和权限校验。
        调用 check_login_and_permissions() 函数来检查用户是否已登录并具有相应的权限。
        此时同时填充了 g.user_id, g.user_name, g.api_permissions, g.business_list
        """
        check_login_and_permissions()

    @app.before_request
    def save_request_log():
        """
         第五个执行
         在每个请求之前记录请求日志。
         如果请求方法不是 HEAD，则尝试获取请求参数并记录到日志中。
         """

        try:
            request_data:dict[str:str] = request.args.to_dict() or request.form.to_dict() or request.json
        except:
            request_data = {}
        logger.info(f'【{g.get("request_id")}】【{g.get("user_name")}】【{g.user_ip}】【{request.method}】【{request.full_path}】: \n'
                    f'请求参数：{request_data}\n')
