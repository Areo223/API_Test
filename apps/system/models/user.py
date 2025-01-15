from flask import g
from sqlalchemy import String, false, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from apps.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "system_user"
    __tablename__={"comment":"用户表"}

    account:Mapped[str] = mapped_column(String(50),nullable=True,unique=True,index=True,comment="账号")
    password:Mapped[str] = mapped_column(String(50),comment="密码")
    name:Mapped[str] = mapped_column(String(20),nullable=False,comment="姓名")
    status:Mapped[int] = mapped_column(Integer(),default=1,comment="状态,1启用,0禁用")
    business_list:Mapped[str] = mapped_column(JSON,default=[],comment="所有业务线")

    @classmethod
    def is_not_admin(cls):
        return not cls.is_admin()

    @classmethod
    def is_admin(cls):
        return 'admin' in cls.get_current_api_permissions()

    @classmethod
    def get_current_api_permissions(cls):
        return g.api_permissions


