# -*- coding: utf-8 -*-
# 用于为不同的HTTP请求方法和路径设置不同的身份验证类型,并且记录请求方法和路径的映射关系。
from flask import Blueprint as FlaskBlueprint

from apps.enums import AuthType

url_required_map = {}


class Blueprint(FlaskBlueprint):
    """
    自定义的蓝图类，用于为不同的HTTP请求方法和路径设置不同的身份验证类型。

    方法:
        get: 获取资源，支持四种不同的身份验证类型。
        login_get: 获取资源，需要登录身份验证。
        permission_get: 获取资源，需要权限身份验证。
        admin_get: 获取资源，需要管理员身份验证。

        post: 创建资源，支持四种不同的身份验证类型。
        login_post: 创建资源，需要登录身份验证。
        permission_post: 创建资源，需要权限身份验证。
        admin_post: 创建资源，需要管理员身份验证。

        put: 更新资源，支持四种不同的身份验证类型。
        login_put: 更新资源，需要登录身份验证。
        permission_put: 更新资源，需要权限身份验证。
        admin_put: 更新资源，需要管理员身份验证。

        delete: 删除资源，支持四种不同的身份验证类型。
        login_delete: 删除资源，需要登录身份验证。
        permission_delete: 删除资源，需要权限身份验证。
        admin_delete: 删除资源，需要管理员身份验证。
    """

    def get(self, path, *args, auth_type=AuthType.not_auth, **kwargs):
        """
        不需要身份验证

        参数:
            path (str): 请求的路径。
            auth_type (AuthType): 身份验证类型，默认为不需要身份验证。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        url_required_map[f'GET_{path}'] = auth_type  # 记录此 请求方法+路径 的身份验证类型
        return super(Blueprint, self).route(path, methods=["GET"], **kwargs)

    def login_get(self, path, *args, **kwargs):
        """
        登录验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.get(path, auth_type=AuthType.login, *args, **kwargs)

    def permission_get(self, path, *args, **kwargs):
        """
        需要接口权限验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.get(path, auth_type=AuthType.permission, *args, **kwargs)

    def admin_get(self, path, *args, **kwargs):
        """
        管理员验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.get(path, auth_type=AuthType.admin, *args, **kwargs)

    def post(self, path, *args, auth_type=AuthType.not_auth, **kwargs):
        """
        不需要身份验证

        参数:
            path (str): 请求的路径。
            auth_type (AuthType): 身份验证类型，默认为不需要身份验证。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        url_required_map[f'POST_{path}'] = auth_type  # 记录此 请求方法+路径 的身份验证类型
        return super(Blueprint, self).route(path, methods=["POST"], **kwargs)

    def login_post(self, path, *args, **kwargs):
        """
        登录验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.post(path, auth_type=AuthType.login, *args, **kwargs)

    def permission_post(self, path, *args, **kwargs):
        """
        需要接口权限验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.post(path, auth_type=AuthType.permission, *args, **kwargs)

    def admin_post(self, path, *args, **kwargs):
        """
        管理员验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.post(path, auth_type=AuthType.admin, *args, **kwargs)

    def put(self, path, *args, auth_type=AuthType.not_auth, **kwargs):
        """
        不需要身份验证

        参数:
            path (str): 请求的路径。
            auth_type (AuthType): 身份验证类型，默认为不需要身份验证。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        url_required_map[f'PUT_{path}'] = auth_type  # 记录此 请求方法+路径 的身份验证类型
        return super(Blueprint, self).route(path, methods=["PUT"], **kwargs)

    def login_put(self, path, *args, **kwargs):
        """
        登录验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.put(path, auth_type=AuthType.login, *args, **kwargs)

    def permission_put(self, path, *args, **kwargs):
        """
        需要接口权限验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.put(path, auth_type=AuthType.permission, *args, **kwargs)

    def admin_put(self, path, *args, **kwargs):
        """
        管理员验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.put(path, auth_type=AuthType.admin, *args, **kwargs)

    def delete(self, path, *args, auth_type=AuthType.not_auth, **kwargs):
        """
        不需要身份验证

        参数:
            path (str): 请求的路径。
            auth_type (AuthType): 身份验证类型，默认为不需要身份验证。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        url_required_map[f'DELETE_{path}'] = auth_type  # 记录此 请求方法+路径 的身份验证类型
        return super(Blueprint, self).route(path, methods=["DELETE"], **kwargs)

    def login_delete(self, path, *args, **kwargs):
        """
        登录验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.delete(path, auth_type=AuthType.login, *args, **kwargs)

    def permission_delete(self, path, *args, **kwargs):
        """
        需要接口权限验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.delete(path, auth_type=AuthType.permission, *args, **kwargs)

    def admin_delete(self, path, *args, **kwargs):
        """
        管理员验证的接口

        参数:
            path (str): 请求的路径。

        返回:
            FlaskBlueprint: 返回一个FlaskBlueprint对象，用于注册路由。
        """
        return self.delete(path, auth_type=AuthType.admin, *args, **kwargs)