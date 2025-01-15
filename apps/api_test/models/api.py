
from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from apps.base_model import BaseApi, FuncFiled, HeadersFiled, ParamsFiled, FormDataFiled, JsonDataFiled, StatusFiled, \
    FormUrlencodedFiled, ValidatesFiled, BodyTypeFiled, ExtractsFiled
from apps.enums import ApiMethodEnum, ApiLevelEnum


class ApiMsg(
    BaseApi,FuncFiled,HeadersFiled,ParamsFiled,
    FormDataFiled,JsonDataFiled,ValidatesFiled,ExtractsFiled,
    BodyTypeFiled,StatusFiled,FormUrlencodedFiled):
    __abstract__ = False
    __tablename__ = "api_test_api"
    __table_args__ = {"comment": "接口测试接口信息表"}

    timeout:Mapped[int] = mapped_column(Integer(),default=60,comment="api请求超时时间,默认60s")
    addr:Mapped[str] = mapped_column(String(1024),nullable=False,comment="api请求地址")
    method:Mapped[ApiMethodEnum] = mapped_column(default=ApiMethodEnum.GET,comment="请求方法")
    level:Mapped[ApiLevelEnum] = mapped_column(default=ApiLevelEnum.LEVEL_1,comment="接口等级:L1,L2,L3")
    data_text:Mapped[str] = mapped_column(Text(),nullable=True,default="",comment="文本参数")
    response:Mapped[dict] = mapped_column(JSON,default={},comment="响应结果")
    use_count:Mapped[int] = mapped_column(Integer(),default=0,comment="使用次数,有多少个step使用了这个api")