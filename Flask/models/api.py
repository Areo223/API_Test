
from Flask.exts import db
from base.base_models import BaseModel


class Api(BaseModel):
    __tablename__ = 'api'
    # __table_args__ = {'comment':"接口测试接口信息表"}
    __table_args__ = {'comment':"接口测试接口信息表",'extend_existing': True}

    # 接口名
    api_name = db.Column(db.String(50), nullable=False)
    # 请求方法
    method = db.Column(db.String(20), default='get', nullable=False)
    # 接口地址
    url = db.Column(db.String(100), default='/', nullable=False)
    # 请求参数
    parametrize = db.Column(db.String(100), nullable=True)
    # JSON
    json = db.Column(db.Text, nullable=True)
    # expect期望返回结果
    expect = db.Column(db.Text, nullable=False)
    # 备注
    description = db.Column(db.Text, nullable=True)

    def __init__(self, api_name, method, url, parametrize, json, expect, description):
        self.api_name = api_name # 接口名
        self.method = method # 请求方法
        self.url = url
        self.parametrize = parametrize
        self.json = json
        self.expect = expect
        self.description = description
    # @classmethod
    # def set_basic_api(cls,api_name,method,url,parametrize,json,expect):
    #     cls.api_name = api_name
    #     cls.method = method
    #     cls.url = url
    #     cls.parametrize = parametrize
    #     cls.json = json
    #     cls.expect = expect
    #     return cls

