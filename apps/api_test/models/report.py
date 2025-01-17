from apps.base_model import BaseReport


class ApiReport(BaseReport):
    __abstract__ = False
    __tablename__ = "api_test_report"
    __table_args__ = {"comment": "接口测试报告表"}
