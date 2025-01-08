from datetime import datetime

from flask import g
from flask_sqlalchemy import query as base_query
from exts import db



class Query(base_query.Query):
    """ 重写query方法，使其默认加上status=0 """

    def filter_by(self, **kwargs):
        """ 如果传过来的参数中不含is_delete，则默认加一个is_delete参数，状态为0 查询有效的数据"""
        # kwargs.setdefault("is_delete", 0)
        return super(Query, self).filter_by(**kwargs)

    def update(self, values, synchronize_session="evaluate", update_args=None):
        try:
            values["update_user"] = g.user_id  # 自动加上更新者id
        except:
            pass
        return super(Query, self).update(values, synchronize_session=synchronize_session, update_args=update_args)

class BaseModel(db.Model):
    """ 基类模型 """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    created_by = db.Column(db.Integer, default=0, nullable=False)
    updated_by = db.Column(db.Integer, default=0, nullable=False)

    @classmethod
    def get_table_column_name_list(cls):
        """ 获取当前表的所有字段 """
        return [column.name for column in cls.__table__.columns]

    @classmethod
    def get_id_list(cls, **kwargs):
        return [data[0] for data in cls.query.with_entities(cls.id).filter_by(**kwargs).all()]

    # @classmethod
    # def format_insert_data(cls, data_dict):
    #     if "id" in data_dict:
    #         data_dict.pop("id")
    #
    #     if cls.__name__ == "User" and "password" in data_dict:
    #         data_dict["password"] = generate_password_hash(data_dict["password"])
    #
    #     try:  # 执行初始化脚本、执行测试时，不在上下文中，不能使用g对象
    #         if hasattr(g, 'user_id') and g.user_id:
    #             current_user = g.user_id  # 真实用户
    #         else:
    #             from apps.system.model_factory import User
    #             current_user = User.db.session.query(User.id).filter(User.account == "common").first()[0]
    #     except Exception as error:
    #         current_user = None
    #     data_dict["create_user"] = data_dict["update_user"] = current_user
    #     data_dict["create_time"] = data_dict["update_time"] = None
    #
    #     # 只保留模型中有的字段
    #     return {key: value for key, value in data_dict.items() if key in cls.get_table_column_name_list()}

    @classmethod
    def model_create(cls, data_dict: dict):
        """ 创建数据 """
        column_name_list = cls.get_table_column_name_list()
        if "num" in column_name_list:  # 如果有num字段，自动获取最大的num，并赋值
            data_dict["num"] = cls.get_insert_num()

        insert_dict = cls.format_insert_data(data_dict)
        with db.auto_commit():
            db.session.add(cls(**insert_dict))

    # @classmethod
    # def model_create_and_get(cls, data_dict: dict):
    #     """ 创建并返回数据，会多一次查询 """
    #     cls.model_create(data_dict)
    #     query_filter = {}
    #     if "name" in data_dict:
    #         query_filter["name"] = data_dict["name"]
    #     if "sso_user_id" in data_dict:
    #         query_filter["sso_user_id"] = data_dict["sso_user_id"]
    #     if "module_id" in data_dict:
    #         query_filter["module_id"] = data_dict["module_id"]
    #     if "parent" in data_dict:
    #         query_filter["parent"] = data_dict["parent"]
    #     if "project_id" in data_dict:
    #         query_filter["project_id"] = data_dict["project_id"]
    #     if "batch_id" in data_dict:
    #         query_filter["batch_id"] = data_dict["batch_id"]
    #     if "report_id" in data_dict:
    #         query_filter["report_id"] = data_dict["report_id"]
    #     if "report_case_id" in data_dict:
    #         query_filter["report_case_id"] = data_dict["report_case_id"]
    #     if "url" in data_dict:
    #         query_filter["url"] = data_dict["url"]
    #     if "method" in data_dict:
    #         query_filter["method"] = data_dict["method"]
    #     if "project" in data_dict:
    #         query_filter["project"] = data_dict["project"]
    #     return cls.query.filter_by(**query_filter).order_by(cls.id.desc()).first()

    # @classmethod
    # def model_batch_create(cls, data_list: list):
    #     """ 批量插入 """
    #     with db.auto_commit():
    #         obj_list = []
    #         for data_dict in data_list:
    #             insert_dict = cls.format_insert_data(data_dict)
    #             obj_list.append(cls(**insert_dict))
    #         db.session.add_all(obj_list)
    #
    # def model_update(self, data_dict: dict):
    #     """ 更新数据 """
    #     if "num" in data_dict: data_dict.pop("num")
    #     if "id" in data_dict: data_dict.pop("id")
    #     if self.__class__.__name__ == "User" and "password" in data_dict:
    #         data_dict["password"] = generate_password_hash(data_dict["password"])
    #     try:
    #         data_dict["update_user"] = g.user_id if hasattr(g, "user_id") else None
    #     except:
    #         pass
    #     with db.auto_commit():
    #         for key, value in data_dict.items():
    #             if hasattr(self, key):
    #                 setattr(self, key, value)

    # @classmethod
    # def batch_update(cls, data_list):
    #     """ 批量更新 """
    #     for data in data_list:
    #         if "id" not in data:
    #             raise "batch_update 方法必须有id字段"
    #         data["update_user"] = g.user_id if hasattr(g, "user_id") else None
    #     cls.db.session.bulk_update_mappings(cls, data_list)
    #
    # def delete(self):
    #     """ 删除单条数据 """
    #     with db.auto_commit():
    #         db.session.delete(self)
    #
    # @classmethod
    # def delete_by_id(cls, data_id):
    #     """ 根据id删除数据 """
    #     if isinstance(data_id, int):
    #         cls.query.filter(cls.id == data_id).delete()
    #     elif isinstance(data_id, list):
    #         cls.query.filter(cls.id.in_(data_id)).delete()
    #
    # @classmethod
    # def get_simple_filed_list(cls):
    #     return [cls.id, cls.name]
    #
    # def enable(self):
    #     """ 启用数据 """
    #     with db.auto_commit():
    #         self.status = DataStatusEnum.ENABLE.value
    #
    # def disable(self):
    #     """ 禁用数据 """
    #     with db.auto_commit():
    #         self.status = DataStatusEnum.DISABLE.value
    #
    # def is_enable(self):
    #     """ 判断数据是否为启用状态 """
    #     return self.status == DataStatusEnum.ENABLE.value
    #
    # def is_disable(self):
    #     """ 判断数据是否为禁用状态 """
    #     return self.status == DataStatusEnum.DISABLE.value
    #
    # @classmethod
    # def format_with_entities_query_list(cls, query_list):
    #     """ 格式化查询集 [(1,), (2,)] -> [1, 2] """
    #     return [res[0] for res in query_list]
    #
    # def current_is_create_user(self):
    #     """ 判断当前传进来的id为数据创建者 """
    #     return self.create_user == g.user_id
    #
    # def copy(self):
    #     """ 复制本身对象 """
    #     data = self.to_dict()
    #     data["name"] = data.get("name") + "_copy" if data.get("name") else "_copy"
    #     if data.get("status"): data["status"] = 0
    #     return self.__class__.model_create(data)
    #
    # @classmethod
    # def get_from_path(cls, data_id):
    #     """ 获取模块/用例集的归属 """
    #     from_name = []
    #
    #     def get_from(current_data_id):
    #         parent_name, parent_parent = cls.query.with_entities(
    #             cls.name, cls.parent).filter(cls.id == current_data_id).first()  # (qwe, 1)
    #         from_name.insert(0, parent_name)
    #
    #         if parent_parent:
    #             get_from(parent_parent)
    #
    #     get_from(data_id)
    #     return '/'.join(from_name)
    #
    # @classmethod
    # def change_sort(cls, id_list, page_num, page_size):
    #     """ 批量修改排序 """
    #     id_list_query = cls.query.with_entities(cls.id).filter(cls.id.in_(id_list)).all()
    #     db_id_list, update_data_list = [id_query[0] for id_query in id_list_query], []
    #     if id_list:
    #         for index, data_id in enumerate(id_list):
    #             if data_id in db_id_list:
    #                 update_data_list.append({"id": data_id, "num": (page_num - 1) * page_size + index})
    #         cls.db.session.bulk_update_mappings(cls, update_data_list)
    #
    # @classmethod
    # def get_max_num(cls, **kwargs):
    #     """ 返回 model 表中**kwargs筛选条件下的已存在编号num的最大值 """
    #     max_num_data = cls.query.filter_by(**kwargs).order_by(cls.num.desc()).first()
    #     return max_num_data.num if max_num_data and max_num_data.num else 0
    #
    # @classmethod
    # def get_insert_num(cls, **kwargs):
    #     """ 返回 model 表中**kwargs筛选条件下的已存在编号num的最大值 + 1 """
    #     return cls.get_max_num(**kwargs) + 1
    #
    # @classmethod
    # def get_current_business_list(cls):
    #     """ 管理员权限 """
    #     return g.business_list
    #
    # @classmethod
    # def get_current_api_permissions(cls):
    #     """ 管理员权限 """
    #     return g.api_permissions
    #
    # @classmethod
    # def is_admin(cls):
    #     """ 管理员权限 """
    #     return 'admin' in cls.get_current_api_permissions()
    #
    # @classmethod
    # def is_not_admin(cls):
    #     """ 非管理员权限 """
    #     return not cls.is_admin()
    #
    # @classmethod
    # def get_first(cls, **kwargs):
    #     """ 获取第一条数据 """
    #     return cls.query.filter_by(**kwargs).first()
    #
    # @classmethod
    # def get_all(cls, **kwargs):
    #     """ 获取全部数据 """
    #     return cls.query.filter_by(**kwargs).all()
    #
    # def to_dict(self, pop_list: list = [], filter_list: list = []):
    #     """ 自定义序列化器
    #     pop_list: 序列化时忽略的字段
    #     filter_list: 仅要序列化的字段
    #     当 pop_list 与 filter_list 同时包含同一个字段时，以 filter_list 为准
    #     """
    #     if pop_list or filter_list:
    #         dict_data = {}
    #         for column_name in self.get_table_column_name_list():
    #             if filter_list:
    #                 if column_name in filter_list:
    #                     dict_data[column_name] = getattr(self, column_name)
    #             else:
    #                 if column_name not in pop_list:
    #                     dict_data[column_name] = getattr(self, column_name)  # self.get_column_data(column_name)
    #         return dict_data
    #     return {column.name: getattr(self, column.name, None) for column in self.__table__.columns}
    #
    # @classmethod
    # def make_pagination(cls, form, get_filed: list = [], order_by=None, **kwargs):
    #     """ 执行分页查询 """
    #     # 排序
    #     if order_by is None:
    #         # 有num就用num升序，否则用id降序
    #         order_by = cls.num.asc() if "num" in cls.get_table_column_name_list() else cls.id.desc()
    #
    #     get_filed = get_filed or cls.__table__.columns  # 如果没传指定字段，则默认查全部字段
    #     col_name_list = [column.name for column in get_filed]  # 字段名
    #
    #     if form.page_num and form.page_size:
    #         query_obj = cls.db.session.query(*get_filed).filter(*form.get_query_filter(**kwargs)).order_by(order_by)
    #         query_result = query_obj.paginate(page=form.page_num, per_page=form.page_size, error_out=False)
    #         return {
    #             "total": query_result.total,
    #             "data": [dict(zip(col_name_list, item)) for item in query_result.items]
    #         }
    #
    #     all_data = cls.db.session.query(*get_filed).filter(*form.get_query_filter(**kwargs)).order_by(order_by).all()
    #     return {
    #         "total": len(all_data),
    #         "data": [dict(zip(col_name_list, item)) for item in all_data]
    #     }

class StatusFiledModel(BaseModel):
    __abstract__ = True
    status = db.Column(db.Integer, nullable=False, default=0)
