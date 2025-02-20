from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from apps.base_model import BaseCase


class ApiCase(BaseCase):
    __abstract__ = False
    __tablename__ = 'api_test_case'
    __table_args__ = {'comment': '接口测试用例信息表'}

    headers:Mapped[dict] = mapped_column(JSON,default=[{
        "key":"","value":"","remark":""
    }],comment="用例请求头")