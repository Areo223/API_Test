
from flask import current_app as _app, request, g
from pydantic import ValidationError


def register_errorhandler_hooks(app):

    @app.errorhandler(400)
    def bad_request(e):
        return _app.restful.fail(e.description)
    @app.errorhandler(401)
    def unauthorized(e):
        return _app.restful.not_login()
    @app.errorhandler(403)
    def forbidden(e):
        return _app.restful.not_permission()
    @app.errorhandler(404)
    def page_not_found(e):
        if request.method != "HEAD":
            _app.logger.exception(f'【{g.get("request_id")}】404错误: {request.path}')
        return _app.restful.not_found(f'接口 {request.path} 不存在')
    @app.errorhandler(405)
    def method_error(e):
        if request.method != "HEAD":
            _app.logger.exception(f'【{g.get("request_id")}】405错误: {request.method} {request.path}')
        return _app.restful.method_not_allowed()
    @app.errorhandler(500)
    def internal_server_error(e):
        if request.method!= "HEAD":
            _app.logger.exception(f'【{g.get("request_id")}】500错误: {request.path}')

    @app.errorhandler(ValidationError)
    def validation_error(exc):
        """
        处理 pydantic 数据校验不通过的异常

        参数:
        exc (ValidationError): 捕获到的异常对象

        返回:
        response (Response): 错误响应对象
        """
        # 获取异常中的第一个错误信息
        error = exc.errors()[0]
        # 从错误信息中提取请求数据、字段名、错误类型和错误消息
        request_data, filed_name, error_type, msg = error["input"], error["loc"][-1], error["type"], error["msg"]
        # 根据字段名获取字段标题
        filed_title = g.current_from.get_filed_title(filed_name)

        # 根据错误类型返回不同的错误响应
        if "type" in error_type or error_type == "int_parsing":  # 数据类型错误
            return _app.restful.fail(f'{filed_title} 数据类型错误')
        elif "required" in msg:  # 必传字段
            return _app.restful.fail(f'{filed_title} 必传')
        elif "value_error" in error_type:  # 数据验证不通过
            # 'Value error, 服务名【xxxx】已存在'
            return _app.restful.fail(msg.split(', ', 1)[1])
        elif "enum" in error_type:  # 枚举错误
            return _app.restful.fail(f'{filed_title} 枚举错误：{msg}')
        elif "max_length" in error_type:  # 数据长度超长
            return _app.restful.fail(f'{filed_title} 长度超长，最多{error["ctx"]["min_length"]}位')
        elif msg == "List should have at least 1 item after validation, not 0":  # 空列表
            return _app.restful.fail(f'最少选择{error["ctx"]["min_length"]}个{filed_title}')
        elif "string_too_short" in error_type:  # 数据长度不够
            return _app.restful.fail(f'{filed_title} 长度不够，最少{error["ctx"]["min_length"]}位')

        # 如果以上条件都不满足，返回一个通用的错误响应
        return _app.restful.fail(f'系统错误：{error}')

    @app.errorhandler(ValueError)
    def value_error(exc):
        """
        处理 ValueError 异常

        参数:
        exc (ValueError): 捕获到的异常对象

        返回:
        response (Response): 错误响应对象
        """
        # 返回一个通用的错误响应
        return _app.restful.fail(f'系统错误：{exc.args[0]}')

    @app.errorhandler(Exception)
    def exception_error(exc):
        """
        处理 Exception 异常
        参数:
        exc (Exception): 捕获到的异常对象
        返回:
        response (Response): 错误响应对象
        """
        # 返回一个通用的错误响应
        return _app.restful.fail(f'系统错误：{exc}')