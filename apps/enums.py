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

class UserRoleEnum(str, BaseEnum):
    """ 用户角色 """
    ADMIN = "admin"
    USER = "user"

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

class CaseStatusEnum(int, BaseEnum):
    """ 测试用例状态 """
    NOT_DEBUG_AND_NOT_RUN = 0  # 未调试-不执行
    DEBUG_PASS_AND_RUN = 1  # 调试通过-要执行
    DEBUG_PASS_AND_NOT_RUN = 2  # 调试通过-不执行
    NOT_DEBUG_PASS_AND_NOT_RUN = 3  # 调试不通过-不执行

class ApiCaseSuiteTypeEnum(str, BaseEnum):
    """ 用例集类型 """
    api = "api"  # 单接口用例集
    base = "base"  # 基础用例集
    quote = "quote"  # 引用用例集
    process = "process"  # 流程用例集
    make_data = "make_data"  # 造数据用例集
