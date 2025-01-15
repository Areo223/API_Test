from contextlib import contextmanager
from datetime import datetime
from typing import Any, Self, Dict, Optional

from flask import g,request
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query as BaseQuery
from sqlalchemy import MetaData, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash

from apps.enums import DataStatusEnum, ApiBodyTypeEnum
from utils.util.json_util import JsonUtil


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):

    def filter_by(self, **kwargs: Any) -> Self:
        """ 如果传过来的参数中不含is_delete，则默认加一个is_delete参数，状态为0 查询有效的数据"""
        # kwargs.setdefault("is_delete", 0)
        return super(Query,self).filter_by(**kwargs)

    def update(
        self,
        values,
        synchronize_session = "evaluate",
        update_args: Optional[Dict[Any, Any]] = None,
    ) -> int:
        """
                更新数据库记录，并自动添加更新者的ID。

                参数:
                    values (dict): 要更新的字段和值的字典。
                    synchronize_session (str): 同步会话的策略，默认为 "evaluate"。
                    update_args (dict): 额外的更新参数。

                返回:
                    执行更新操作的结果。

                异常:
                    - 如果在尝试获取更新者ID时发生异常，会被忽略。
                """
        try:
            values["update_user"] = g.user.id
        except:
            pass
        return super(Query,self).update(values,synchronize_session=synchronize_session,update_args=update_args)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(
    query_class=Query,
    metadata=MetaData(naming_convention=naming_convention)
)

class BaseModel(db.Model,JsonUtil):
    __abstract__ = True
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "comment": "基础模型"
    }
    db = db
    id:Mapped[int] = mapped_column(Integer(),primary_key=True,comment="主键,自增")
    create_time:Mapped[DateTime] = mapped_column(DateTime(),nullable=True,default=datetime.now,comment="创建时间")
    create_user:Mapped[int] = mapped_column(Integer(),nullable=True,default=None,comment="创建人")
    update_time:Mapped[DateTime] = mapped_column(DateTime(),nullable=True,default=datetime.now,comment="更新时间")
    update_user:Mapped[int] = mapped_column(Integer(),nullable=True,default=None,comment="更新人")

    def model_update(self, data_dict: dict):
        """
         更新数据
         去除id字段，去除num字段，自动加密password字段，自动获取update_user字段
         """
        if "num" in data_dict: data_dict.pop("num")
        if "id" in data_dict: data_dict.pop("id")
        if self.__class__.__name__ == "User" and "password" in data_dict:
            data_dict["password"] = generate_password_hash(data_dict["password"])
        try:
            data_dict["update_user"] = g.user_id if hasattr(g, "user_id") else None
        except:
            pass
        with db.auto_commit():
            for key, value in data_dict.items():
                if hasattr(self, key):
                    setattr(self, key, value)


class StatusFiled(BaseModel):
    __abstract__ = True
    status:Mapped[int] = mapped_column(Integer(),nullable=True,default=DataStatusEnum.ENABLE.value,comment="状态,1:启用,0:禁用")

class NumFiled(BaseModel):
    __abstract__ = True
    num:Mapped[int] = mapped_column(Integer(),nullable=True,default=0,comment="排序")

class BaseApi(StatusFiled,NumFiled):
    __abstract__ = True

    name:Mapped[str] = mapped_column(String(20),nullable=True,comment="名称")
    desc:Mapped[str] = mapped_column(Text(),nullable=True,default="",comment="描述")
    project_id:Mapped[int] = mapped_column(Integer(),nullable=True,default=None,index=True,comment="项目ID")
    module_id:Mapped[int] = mapped_column(Integer(),nullable=True,default=None,index=True,comment="模块ID")

class FuncFiled(BaseModel):
    __abstract__ = True

    up_func:Mapped[str] = mapped_column(JSON,default=[],comment="前置函数")
    down_func:Mapped[str] = mapped_column(JSON,default=[],comment="后置函数")

class HeadersFiled(BaseModel):
    __abstract__ = True

    headers:Mapped[list] = mapped_column(JSON,default=[{"key":None,"remark":None,"value":None}],comment="请求头")

class ParamsFiled(BaseModel):
    __abstract__ = True
    params:Mapped[list] = mapped_column(JSON,default=[{"key":None,"value":None}],comment="params参数")

class FormDataFiled(BaseModel):
    __abstract__ = True
    form_data:Mapped[list] = mapped_column(JSON, default=[{"data_type":None, "key":None, "remark":None, "value":None}], comment="form_data参数")

class JsonDataFiled(BaseModel):
    __abstract__ = True
    json_data:Mapped[dict] = mapped_column(JSON,default={},comment="json参数")

class ValidatesFiled(BaseModel):
    __abstract__ = True
    validates:Mapped[list] = mapped_column(
        JSON,
        default=[{
            "status":0,
            "key":None,
            "value":None,
            "remark":None,
            "data_type":None,
            "data_source":None,
            "validate_method":None,
            "validate_type":"data"
        }],comment="断言")

class FormUrlencodedFiled(BaseModel):
    __abstract__ = True
    form_urlencoded:Mapped[dict] = mapped_column(JSON,default={},comment="form_urlencoded参数")

class BodyTypeFiled(BaseModel):
    __abstract__ = True
    body_type:Mapped[ApiBodyTypeEnum] = mapped_column(default=ApiBodyTypeEnum.json.value,comment="body数据类型,json/form/text/urlencoded")

class ExtractsFiled(BaseModel):
    __abstract__ = True
    extracts:Mapped[list] = mapped_column(
        JSON,
        default=[{
        "status":0,
        "key":None,
        "value":None,
        "remark":None,
        "data_source":None,
        "update_to_header":None
    }],comment="提取参数")

class BaseModule(NumFiled):
    __abstract__ = True
    name:Mapped[str] = mapped_column(String(255),nullable=False,comment="名称")
    parent:Mapped[int] = mapped_column(Integer(),nullable=True,default=None,comment="父级ID")
    project_id:Mapped[int] = mapped_column(Integer(),index=False,comment="项目ID")

class BaseProject(StatusFiled,NumFiled):
    __abstract__ = True
    name:Mapped[str] = mapped_column(String(255),unique=True,nullable=False,comment="名称")
    manager:Mapped[int] = mapped_column(Integer(),nullable=False,comment="负责人")
    business_id:Mapped[int] = mapped_column(Integer(),nullable=False,index=True,comment="业务线")
