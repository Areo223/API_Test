
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

    time_out:Mapped[int] = mapped_column(Integer(),default=60,comment="api请求超时时间,默认60s")
    addr:Mapped[str] = mapped_column(String(1024),nullable=False,comment="api请求地址")
    method:Mapped[ApiMethodEnum] = mapped_column(default=ApiMethodEnum.GET,comment="请求方法")
    level:Mapped[ApiLevelEnum] = mapped_column(default=ApiLevelEnum.LEVEL_1,comment="接口等级:L1,L2,L3")
    data_text:Mapped[str] = mapped_column(Text(),nullable=True,default="",comment="文本参数")
    response:Mapped[dict] = mapped_column(JSON,default={},comment="响应结果")
    use_count:Mapped[int] = mapped_column(Integer(),default=0,comment="使用次数,有多少个step使用了这个api")

    @classmethod
    def make_pagination(cls,form,get_filed:list,order_by=None,**kwargs):
        """ 执行分页查询 """
        # 排序
        if order_by is None:
            # 有num就用num升序，否则用id降序
            # NumFiled为带num的基类
            order_by = cls.num.asc() if "num" in cls.get_table_column_name_list() else cls.id.desc()

        get_filed = get_filed or cls.__table__.columns  # 如果没传指定字段，则默认查全部字段
        # get_filed 是一个装有 Column 类对象的列表,因此通过Column.name获取字段名
        col_name_list = [column.name for column in get_filed]  # 字段名列表
        # 从表单中获取分页参数
        if form.page_num and form.page_size:
            # 调用session分页查询
            # query_obj 是一个Query对象
            # 这里的form.get_query_filter(**kwargs)是一个列表,装着查询条件的列表,如Project.name == "test"
            query_obj \
                = (cls.db.session.query(*get_filed).filter(*form.get_query_filter(**kwargs)).order_by(order_by))
            # 继续调用query_obj的分页方法
            # 得到的query_result 是一个Paginate对象
            query_result = query_obj.paginate(page=form.page_num, per_page=form.page_size, error_out=False)
            return {
                # 总数
                "total": query_result.total,
                # 数据
                # zip()作用是将所有的item填充到key为col_name_list的键值对中
                # query_result.items 是一个列表,装着当前页所有记录
                "data": [dict(zip(col_name_list, item)) for item in query_result.items]
                # 'data': [{'id': 1, 'name': 'test', 'swagger': None, 'last_pull_status': 1, 'business_id': 1, 'manager': 1, 'update_user': 1}]
            }

        # 不分页
        # 最后多了一个all()方法,返回的是一个列表
        all_data = cls.db.session.query(*get_filed).filter(*form.get_query_filter(**kwargs)).order_by(order_by).all()
        return {
            "total": len(all_data),
            "data": [dict(zip(col_name_list, item)) for item in all_data]
        }
