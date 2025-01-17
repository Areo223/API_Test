import jwt
from flask import request, current_app as app, g, abort

from apps.enums import AuthType



def parse_access_token(token):
    """
    解析访问令牌。
    此函数用于解析访问令牌。
    参数:
        token (str): 访问令牌字符串。
    返回:
        bool: 如果令牌有效且未过期，则返回 True；否则返回 False。
    """
    try:
        data = jwt.decode(token, app.config["ACCESS_TOKEN_SECRET_KEY"], algorithms=["HS256"])
        g.user_id = data.get("id")
        g.user_name = data.get("name")
        g.api_permissions = data.get("permissions")
        g.business_list = data.get("business_list")
        return True
    except:
        return False

def check_login_and_permissions():
    """
    检查用户是否已登录并具有相应的权限。
    此函数首先检查用户是否已登录（通过检查 g.user_id 是否存在）。
    如果用户已登录，则根据用户的角色和权限进行进一步的检查。
    如果用户未登录，则返回 False。
    返回:
    """

    from apps.system.models.user import User


    request_url = request.path.split("/",2)[-1]
    auth_type = app.url_required_map.get(f'{request.method}/{request_url}')

    parse_access_token(request.headers.get("access_token"))

    if auth_type != AuthType.not_auth:
        if auth_type == AuthType.login:
            if not g.user_id:
                abort(401)

        elif auth_type == AuthType.permission:
            if User.is_not_admin() and request_url not in g.api_permissions:
                abort(403)

        elif auth_type == AuthType.admin:
            if User.is_not_admin():
                abort(403)