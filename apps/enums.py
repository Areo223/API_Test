from enum import Enum


class BaseEnum(Enum):
    """ 枚举基类 """
    @classmethod
    def values(cls):
        """ 获取枚举值列表 """
        return [item.value for item in cls]
    @classmethod
    def choices(cls):
        """ 获取枚举选项列表 """
        return [(item.value, item.name) for item in cls]



class AuthType(str, BaseEnum):
    """ 身份验证类型 """
    login = "login"
    permission = "permission"
    admin = "admin"
    not_auth = "not_auth"
class DataStatusEnum(str, BaseEnum):
    """ 数据状态枚举 """
    ENABLE = 1
    DISABLE = 2

class ApiBodyTypeEnum(str, BaseEnum):
    """ 请求体类型 """
    none = ""
    raw = "raw"
    json = "json"
    form = "form"
    text = "text"
    urlencoded = "urlencoded"

class ApiMethodEnum(str, BaseEnum):
    """ 请求方法 """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class ApiLevelEnum(str, BaseEnum):
    """ 接口级别 """
    # 最高优先级
    LEVEL_0 = "L0"
    # 一般优先级
    LEVEL_1 = "L1"
    # 最低优先级
    LEVEL_2 = "L2"

class ProjectLastPullStatusEnum(str, BaseEnum):
    """ 项目最后一次拉取状态 """
    SUCCESS = 2
    FAIL = 0
    NOT_PULL = 1