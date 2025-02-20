from datetime import datetime

import jwt
from flask import g,current_app as app
from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash

from apps.base_model import BaseModel
from apps.enums import UserRoleEnum


class User(BaseModel):
    __tablename__ = "system_user"
    __table_args__={"comment":"用户表"}

    account:Mapped[str] = mapped_column(String(50),nullable=True,unique=True,index=True,comment="账号")
    password:Mapped[str] = mapped_column(String(50),comment="密码")
    name:Mapped[str] = mapped_column(String(20),nullable=False,comment="姓名")
    status:Mapped[int] = mapped_column(Integer(),default=1,comment="状态,1启用,0禁用")
    business_list:Mapped[str] = mapped_column(JSON,default=[],comment="所有业务线")
    role:Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.USER.value,comment="角色")

    @classmethod
    def is_not_admin(cls):
        return not cls.is_admin()

    @classmethod
    def is_admin(cls):
        return 'admin' in cls.get_current_api_permissions()

    @classmethod
    def get_current_api_permissions(cls):
        return g.api_permissions

    def verify_password(self, password):
        """ 校验密码 """
        return check_password_hash(self.password, password)

    def make_access_token(self, api_permissions: list = []):
        """ 生成token，默认有效期为系统配置的时长 """
        user_info = {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "api_permissions": api_permissions,
            "business_list": self.business_list,
            "exp": datetime.now().timestamp() + app.config["ACCESS_TOKEN_TIME_OUT"]
        }
        return jwt.encode(user_info, app.config["ACCESS_TOKEN_SECRET_KEY"])

    def build_access_token(self):
        """ 构建用户的接口权限 """
        # TODO permissions没写
        user_info =self.to_dict()
        user_info["access_token"] = self.make_access_token()
        return user_info

    def make_refresh_token(self):
        user_info = {
            "user_id": self.id,
            "exp": datetime.now().timestamp() + app.config["REFRESH_TOKEN_TIME_OUT"]}
        return jwt.encode(user_info, app.config["REFRESH_TOKEN_SECRET_KEY"])