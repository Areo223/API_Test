from contextlib import contextmanager
from datetime import datetime
from typing import Any, Self, Dict, Optional, Union

from flask import g,request
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query as BaseQuery
from sqlalchemy import MetaData, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from werkzeug.security import generate_password_hash

from apps.enums import DataStatusEnum, ApiBodyTypeEnum, CaseStatusEnum, ApiCaseSuiteTypeEnum
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

    @classmethod
    def model_create_and_get(cls, data_dict: dict):
        """ 创建并返回数据，会多一次查询 """
        # 执行创建数据
        cls.model_create(data_dict)
        query_filter = {}
        if "name" in data_dict:
            query_filter["name"] = data_dict["name"]
        if "sso_user_id" in data_dict:
            query_filter["sso_user_id"] = data_dict["sso_user_id"]
        if "module_id" in data_dict:
            query_filter["module_id"] = data_dict["module_id"]
        if "parent" in data_dict:
            query_filter["parent"] = data_dict["parent"]
        if "project_id" in data_dict:
            query_filter["project_id"] = data_dict["project_id"]
        if "batch_id" in data_dict:
            query_filter["batch_id"] = data_dict["batch_id"]
        if "report_id" in data_dict:
            query_filter["report_id"] = data_dict["report_id"]
        if "report_case_id" in data_dict:
            query_filter["report_case_id"] = data_dict["report_case_id"]
        if "url" in data_dict:
            query_filter["url"] = data_dict["url"]
        if "method" in data_dict:
            query_filter["method"] = data_dict["method"]
        if "project" in data_dict:
            query_filter["project"] = data_dict["project"]
        # 返回查询到的第一个ORM对象
        return cls.query.filter_by(**query_filter).order_by(cls.id.desc()).first()

    @classmethod
    def model_batch_create(cls, data_list: list):
        """
        批量插入
        传入的data_list 是一个列表，列表中的每个元素都是一个字典，字典要对应model
        """
        with db.auto_commit():
            obj_list = []
            for data_dict in data_list:
                # 格式化插入数据
                insert_dict = cls.format_insert_data(data_dict)
                obj_list.append(cls(**insert_dict))
            # 批量添加
            db.session.add_all(obj_list)

    @classmethod
    def get_first(cls,**kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def delete_by_id(cls, data_id):
        """ 根据id删除数据 """
        # 如果是int类型，就删除单条数据
        if isinstance(data_id, int):
            cls.query.filter(cls.id == data_id).delete()
        # 如果是list类型，就批量删除
        elif isinstance(data_id, list):
            cls.query.filter(cls.id.in_(data_id)).delete()

class BaseUser(BaseModel):
    __abstract__ = True
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

class VariablesFiled(BaseModel):
    __abstract__ = True
    variables:Mapped[list] = mapped_column(JSON,default=[
        {
            "key":None,
            "value":None,
            "remark":None,
            "data_type":None
        }
    ],comment="公共参数")

class SkipIfFiled(BaseModel):
    __abstract__ = True
    skip_if:Mapped[list] = mapped_column(JSON,default=[{
        "expect":None,
        "comparator":None,
        "data_source":None,
        "data_type":None,
        "skip_type":None,
        "check_value":None
    }],comment="跳过条件")

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

class BaseCase(VariablesFiled,StatusFiled,NumFiled,SkipIfFiled):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="名称")
    desc: Mapped[str] = mapped_column(Text(), nullable=False, comment="用例描述")
    status: Mapped[int] = mapped_column(
        Integer(), default=CaseStatusEnum.NOT_DEBUG_AND_NOT_RUN.value,
        comment="用例调试状态，0未调试-不执行，1调试通过-要执行，2调试通过-不执行，3调试不通过-不执行，默认未调试-不执行")
    run_times: Mapped[int] = mapped_column(Integer(), default=1, comment="执行次数，默认执行1次")
    output: Mapped[list] = mapped_column(JSON, default=[], comment="用例出参（步骤提取的数据）")
    suite_id: Mapped[int] = mapped_column(Integer(), nullable=False, index=True, comment="所属的用例集id")

class BaseStep(NumFiled,FuncFiled,StatusFiled,SkipIfFiled):
    __abstract__ = True

    run_times: Mapped[int] = mapped_column(Integer(), default=1, comment="执行次数，默认执行1次")
    name = db.Column(db.String(255), nullable=False, comment="步骤名称")
    skip_on_fail: Mapped[int] = mapped_column(
        Integer(), default=1, nullable=True,
        comment="当用例有失败的步骤时，是否跳过此步骤，1跳过，0不跳过，默认跳过")
    data_driver: Mapped[list] = mapped_column(JSON, default=[], comment="数据驱动，若此字段有值，则走数据驱动的解析")
    quote_case: Mapped[int] = mapped_column(Integer(), nullable=True, default=None, comment="引用用例的id")
    case_id: Mapped[int] = mapped_column(Integer(), nullable=False, index=True, comment="步骤所在的用例的id")

class BaseCaseSuite(NumFiled):
    __abstract__ = True

    name:Mapped[str] = mapped_column(String(255),nullable=False,comment="名称")
    suite_type: Mapped[ApiCaseSuiteTypeEnum] = mapped_column(
        default=ApiCaseSuiteTypeEnum.base.value,
        comment="用例集类型，base: 基础用例集，api: 单接口用例集，process: 流程用例集，make_data: 造数据用例集")
    parent: Mapped[int] = mapped_column(Integer(), nullable=True, default=None, comment="上一级用例集id")
    project_id:Mapped[int] = mapped_column(Integer(),nullable=False,index=True,comment="项目ID")

class BaseReport(BaseModel):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="测试报告名称")
    is_passed: Mapped[int] = mapped_column(Integer(), default=1, comment="是否全部通过，1全部通过，0有报错")
    run_type: Mapped[str] = mapped_column(
        String(255), default="task", nullable=True, comment="报告类型，task/suite/case/api")
    status: Mapped[int] = mapped_column(Integer(), default=1, comment="当前节点是否执行完毕，1执行中，2执行完毕")
    retry_count: Mapped[int] = mapped_column(Integer(), default=0, comment="已经执行重试的次数")
    env: Mapped[str] = mapped_column(String(255), default="test", comment="运行环境")
    temp_variables: Mapped[dict] = mapped_column(JSON, default={}, nullable=True, comment="临时参数")
    process: Mapped[int] = mapped_column(Integer(), default=1, comment="进度节点, 1: 解析数据、2: 执行测试、3: 写入报告")
    batch_id: Mapped[str] = mapped_column(String(128), index=True, comment="运行批次id，用于查询报告")
    trigger_id: Mapped[Union[int, list, str]] = mapped_column(JSON, comment="运行id，用于触发重跑")
    project_id: Mapped[int] = mapped_column(Integer(), nullable=False, index=True, comment="所属的服务id")
    summary: Mapped[dict] = mapped_column(JSON, default={}, comment="报告的统计")

