import copy
import time
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
from utils.parse.parse import parse_list_to_dict, update_dict_to_list
from utils.util.json_util import JsonUtil
from config import _main_server_host


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

class BaseProjectEnv(VariablesFiled):
    """ 服务环境基类表 """
    __abstract__ = True
    # host自动获取主服务器的域名,世纪难题解决!
    host: Mapped[str] = mapped_column(String(255), default=_main_server_host, comment="服务地址")
    env_id: Mapped[int] = mapped_column(Integer(), index=True, nullable=False, comment="对应环境id")
    project_id: Mapped[int] = mapped_column(Integer(), index=True, nullable=False, comment="所属的服务id")

    @classmethod
    def create_env(cls, project_env_model=None, run_env_model=None, project_id=None, env_list=None):
        """
        当环境配置更新时，自动给项目/环境增加环境信息
        如果指定了项目id，则只更新该项目的id，否则更新所有项目的id
        如果已有当前项目的信息，则用该信息创建到指定的环境
        """
        # 如果没有指定项目id，也没有指定环境列表，则不更新
        if not project_id and not env_list:
            return
        # 如果指定了env_list就使用,如果没有就从run_env_model中获取
        env_id_list = env_list or run_env_model.get_id_list()
        # 如果指定了项目id，则只更新该项目的id，否则更新所有项目的id
        if project_id:
            # 获取当前项目
            current_project_env = cls.get_first(project_id=project_id)
            # 成功获取到当前项目，则使用该项目,否则使用默认信息
            data = current_project_env.to_dict() if current_project_env else {"project_id": project_id}
            # 最后得到的data是一个字典
            new_env_data_list = []
            # 对于每一个环境id
            for env_id in env_id_list:
                # 把环境id赋值给data字典的"env_id"
                data["env_id"] = env_id
                # deepcopy会递归地复制整个数据结构，创建出完全独立的副本
                new_env_data_list.append(copy.deepcopy(data))
            # 批量创建新的环境
            cls.model_batch_create(new_env_data_list)

        else:
            for project_query_id in project_env_model.get_id_list():
                cls.create_env(project_env_model, run_env_model, project_query_id, env_id_list)

    @classmethod
    def change_env(cls, form):
        """ 修改环境 """
        # 更新当前环境
        form.project_env.model_update(form.model_dump())
        # 更新环境的时候，把环境的头部信息、变量的key一并同步到其他环境
        env_id_list_query = cls.db.session.query(cls.env_id).filter(
            cls.project_id == form.project_id, cls.env_id != form.project_env.env_id).all()
        cls.synchronization(form.project_env, [int(env_id[0]) for env_id in env_id_list_query])

    @classmethod
    def synchronization(cls, from_env, to_env_id_list: list):
        """ 把当前环境同步到其他环境
        from_env: 从哪个环境
        to_env_list: 同步到哪些环境
        """
        # 同步数据来源
        is_update_headers = hasattr(cls, "headers")
        filed_list = ["variables", "headers"] if is_update_headers else ["variables"]

        # 同步数据来源解析
        from_env_dict = {}
        for filed in filed_list:
            from_env_dict[filed] = parse_list_to_dict(getattr(from_env, filed))

        # 同步至指定环境
        new_env_list = []
        to_env_list = cls.db.session.query(cls.id, *[getattr(cls, filed) for filed in filed_list]).filter(
            cls.project_id == from_env.project_id, cls.env_id.in_(to_env_id_list)).all()

        for to_env_data in to_env_list:
            new_env_data = {
                "id": to_env_data[0],
                "variables": update_dict_to_list(from_env_dict["variables"], to_env_data[1])
            }
            if is_update_headers:
                new_env_data["headers"] = update_dict_to_list(from_env_dict["headers"], to_env_data[2])
            new_env_list.append(new_env_data)
        cls.batch_update(new_env_list)

    @classmethod
    def add_env(cls, env_id, project_model):
        """ 新增运行环境时，批量给服务/项目/APP加上 """
        data_list = []
        for project_id in project_model.get_id_list():
            if not cls.db.session.query(cls.id).filter_by(project_id=project_id, env_id=env_id).first():
                data_list.append({"env_id": env_id, "project_id": project_id})
        cls.model_batch_create(data_list)

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

    @classmethod
    def get_batch_id(cls):
        """ 生成运行id """
        return f'{g.user_id}_{int(time.time() * 1000000)}'

    @staticmethod
    def get_summary_template():
        return {
            "result": "success",
            "stat": {
                "test_case": {  # 用例维度
                    "total": 0,  # 初始化的时候给个1，方便用户查看运行中的报告，后续会在流程中更新为实际的total
                    "success": 0,
                    "fail": 0,
                    "error": 0,
                    "skip": 0
                },
                "test_step": {  # 步骤维度
                    "total": 0,
                    "success": 0,
                    "fail": 0,
                    "error": 0,
                    "skip": 0
                },
                "count": {  # 此次运行有多少接口/元素
                    "api": 1,
                    "step": 1,
                    "element": 0
                },
                "response_time": {  # 记录步骤响应速度统计
                    "slow": [],
                    "very_slow": []
                }
            },
            "time": {  # 时间维度
                "start_at": "",
                "end_at": "",
                "step_duration": 0,  # 所有步骤的执行耗时，只统计请求耗时
                "case_duration": 0,  # 所有用例下所有步骤执行耗时，只统计请求耗时
                "all_duration": 0  # 开始执行 - 执行结束 整个过程的耗时，包含测试过程中的数据解析、等待...
            },
            "env": {  # 环境
                "code": "",
                "name": "",
            }
        }

class BaseReportCase(BaseModel):
    """ 用例执行记录基类表 """
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(128), nullable=True, comment="测试用例名称")
    case_id: Mapped[int] = mapped_column(Integer(), nullable=True, index=True, comment="执行记录对应的用例id")
    suite_id: Mapped[int] = mapped_column(Integer(), nullable=True, default=None, comment="执行用例所在的用例集id")
    report_id: Mapped[int] = mapped_column(Integer(), index=True, comment="测试报告id")
    result: Mapped[str] = mapped_column(
        String(128), default='waite',
        comment="步骤测试结果，waite：等待执行、running：执行中、fail：执行不通过、success：执行通过、skip：跳过、error：报错")
    case_data: Mapped[dict] = mapped_column(JSON, default={}, comment="用例的数据")
    summary: Mapped[dict] = mapped_column(JSON, default={}, comment="用例的报告统计")
    error_msg: Mapped[str] = mapped_column(Text(), default='', comment="用例错误信息")

class BaseReportStep(BaseModel):
    """ 步骤执行记录基类表 """
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(128), nullable=True, comment="测试步骤名称")
    case_id: Mapped[int] = mapped_column(Integer(), nullable=True, default=None, comment="步骤所在的用例id")
    step_id: Mapped[int] = mapped_column(Integer(), nullable=True, index=True, default=None, comment="步骤id")
    element_id: Mapped[int] = mapped_column(Integer(), comment="步骤对应的元素/接口id")
    report_case_id: Mapped[int] = mapped_column(Integer(), index=True, nullable=True, default=None,
                                                comment="用例数据id")
    status: Mapped[str] = mapped_column(String(8), default="resume", comment="resume:放行、pause:暂停、stop:中断")
    report_id: Mapped[int] = mapped_column(Integer(), index=True, comment="测试报告id")
    process: Mapped[str] = mapped_column(
        String(128), default='waite',
        comment="步骤执行进度，waite：等待解析、parse: 解析数据、before：前置条件、after：后置条件、run：执行测试、extract：数据提取、validate：断言")
    result: Mapped[str] = mapped_column(
        String(128), default='waite',
        comment="步骤测试结果，waite：等待执行、running：执行中、fail：执行不通过、success：执行通过、skip：跳过、error：报错")
    step_data: Mapped[dict] = mapped_column(JSON, default={}, comment="步骤的数据")
    summary: Mapped[dict] = mapped_column(
        JSON, comment="步骤的统计",
        default={"response_time_ms": 0, "elapsed_ms": 0, "content_size": 0, "request_at": "", "response_at": ""})



