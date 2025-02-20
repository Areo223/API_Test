from apps.base_model import BaseModule


class ApiModule(BaseModule):
    __abstract__ = False
    __tablename__ = 'api_test_module'
    __table_args__ = {'comment': '接口测试模块信息表'}

