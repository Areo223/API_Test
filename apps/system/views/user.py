
import jwt

from apps.system.blueprint import system
from apps.system.form.user import LoginForm
from flask import current_app as app, request, abort

from ..model_factory import User


@system.post("/user/login")
def system_login():
    form = LoginForm()
    user_info = form.user.build_access_token()
    user_info["refresh_token"] = form.user.make_refresh_token()
    return app.restful.success(user_info)

@system.post("/user/refresh")
def system_refresh_token():
    refresh_token = request.headers.get("refresh_token")
    try:
        data = jwt.decode(refresh_token, app.config["c"], algorithms=["HS256"])
        user = User.get_first(id=data.get("user_id"))
        user_info = user.build_access_token()
        return app.restful.get_success(user_info)
    except:
        abort(401)