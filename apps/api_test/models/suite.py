from apps.base_model import BaseCaseSuite


class ApiCaseSuite(BaseCaseSuite):
    __abstract__ = False
    __tablename__ = 'api_test_case_suite'
    __table_args__ = {'comment': '接口测试套件信息表'}