from email.policy import default

from base.base_models import BaseModel
from exts import db


class Api(BaseModel):
    __table_args__ = {'comment':"接口测试接口信息表"}


    # 接口名
    api_name = db.Column(db.String(50), nullable=False)
    # 请求方法
    method = db.Column(db.String(20), default='get', nullable=False)
    # 接口地址
    url = db.Column(db.String(100), default='/', nullable=False)
    # 请求参数
    parametrize = db.Column(db.String(100), nullable=False)
    # JSON
    json = db.Column(db.Text, nullable=False)
    # expect期望返回结果
    expect = db.Column(db.Text, nullable=False)
    # 备注
    description = db.Column(db.Text, nullable=False)
