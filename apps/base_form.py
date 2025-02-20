from typing import Optional, Union

from flask import g, request

from utils.util.json_util import JsonUtil
from pydantic import BaseModel as pydanticBaseModel, Field


class BaseForm(pydanticBaseModel,JsonUtil):
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item, None)

    def __init__(self):
        """
        实例化的时候获取所有参数一起传给BaseForm，pydantic会在实例化的时候自动进行数据校验
        然后这里把所有参数都放到g上，如果报错了，会自动抛出异常，然后在异常处理函数中获取当前的Form异常信息，然后返回给用户
        """
        g.current_from = self  # 初始化的时候把form放g上，方便在处理异常的时候获取字段title，提示用户
        # 先尝试从request中获取json，如果获取不到，就从form(表单)中获取字典，如果还获取不到，就从args(参数)中获取字典
        request_data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
        # 调用父类pydanticBaseModel的初始化方法，将请求数据作为关键字参数传入
        super(BaseForm, self).__init__(**request_data)

        self.depends_validate()  # 自动执行有依赖关系的数据验证

    def depends_validate(self):
        """ 有依赖关系的数据验证，
        由于pydantic的验证顺序不可控，而业务上是存在字段先后和依赖关系的，要求子类重写此方法，在此方法内进行对应的验证
        """

    @classmethod
    def validate_data_is_exist(cls,msg:str = None,**kwargs):
        """
        校验数据是否存在
        :param msg:
        :param db_model:
        :param kwargs:
        :return:数据库对象
        """
        data = cls.get_first(**kwargs)
        if data:
            raise Exception(msg or "数据不存在")
        return data

    @classmethod
    def validate_is_true(cls, data, msg):
        """ 判断为真 """
        if not data:
            raise ValueError(msg)

class PaginationForm(BaseForm):
    """ 分页的模型 """
    page_num: Optional[int] = Field(None, title="页数")
    page_size: Optional[int] = Field(None, title="页码")
    detail: bool = Field(False, title='是否获取详细数据')

class ApiListModel(pydanticBaseModel):
    name: str = Field(..., title="接口名字")
    method: str = Field(..., title="请求方法")
    addr: str = Field(..., title="接口地址")

class ParamModel(pydanticBaseModel):
    """
    参数模型类，用于表示键值对参数。

    属性：
        key (Union[str, None]): 参数的键，可以是字符串或 None。
        value (Union[str, None]): 参数的值，可以是字符串或 None。
    """
    key: Union[str, None] = None
    value: Union[str, None] = None

class HeaderModel(ParamModel):
    """
    定义了一个继承自 ParamModel 的类 HeaderModel，用于表示头部信息模型。

    属性:
        remark (Union[str, None]): 头部信息的备注，类型为字符串或 None，默认值为 None。
    """
    # 定义 remark 字段，默认值为 None
    remark: Union[str, None] = None

class FormDataModel(HeaderModel):
    # 添加了一个新的字段 data_type，类型为字符串或 None，默认值为 None,表示数据类型
    data_type: Union[str, None] = None

class VariablesModel(FormDataModel):
    pass

class ExtractModel(HeaderModel):
    """
    定义一个数据模型类，用于表示数据提取的相关信息。

    继承自 `HeaderModel`，并添加了以下属性：
    - `value`: 提取的值，可以是字符串、整数或空值。
    - `status`: 状态，可以是整数或空值。
    - `data_source`: 数据来源，可以是字符串或空值。
    - `extract_type`: 提取类型，可以是字符串或空值。
    - `update_to_header`: 是否更新到头部，可以是字符串、布尔值、整数或空值。

    """
    # 定义 value 字段，默认值为 None
    value: Optional[Union[str, int, None]] = None
    # 定义 status 字段，默认值为 None
    status: Union[int, None] = None
    # 定义 data_source 字段，默认值为 None
    data_source: Union[str, None] = None
    # 定义 extract_type 字段，默认值为 None
    extract_type: Union[str, None] = None
    # 定义 update_to_header 字段，默认值为 None
    update_to_header: Optional[Union[str, bool, int, None]] = None

class ValidateModel(HeaderModel):
    """
    定义一个数据模型类，用于验证数据的合法性。

    继承自 `HeaderModel`，并添加了以下属性：
    - `status`: 状态，可以是整数或空值。
    _ 'validate_type': 验证类型，可以是字符串或空值。
    - `data_type`: 数据类型，可以是字符串或空值。
    _ 'data_source': 数据来源，可以是字符串或空值。
    _ 'validate_method': 验证方法，可以是字符串或空值。
    Attributes:
        status (Union[str, int, None]): 状态字段，用于表示数据的状态，可为字符串、整数或空值。
    """
    # 定义 status 字段，默认值为 None
    status: Union[str, int, None] = None
    validate_type: Union[str, int, None] = None
    data_type: Union[str, int, None] = None
    data_source: Union[str, int, None] = None
    validate_method: Union[str, int, None] = None
