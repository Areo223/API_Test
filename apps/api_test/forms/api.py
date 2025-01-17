from typing import Optional, List, Union

from pydantic import Field, field_validator
from ..model_factory import ApiMsg as Api,ApiCase as Case,ApiStep as Step
from apps.base_form import PaginationForm, BaseForm, ApiListModel, ExtractModel, ValidateModel, HeaderModel, ParamModel, \
    FormDataModel
from ...enums import DataStatusEnum, ApiBodyTypeEnum, ApiLevelEnum


class ApiListForm(PaginationForm):
    """ 查询接口列表 """
    module_id: int = Field(...,title="模块id")
    name: Optional[str] = Field(None,title="接口名称")

class GetApiForm(BaseForm):
    """ 获取api信息 """
    id: int = Field(..., title="接口id")

    @field_validator('id')
    def validate_id(self, value):
        api = self.validate_data_is_exist("接口不存在",id=value)
        setattr(self, 'api', api)
        return value

class ChangeStatusForm(GetApiForm):
    """ 修改接口状态 """
    status: DataStatusEnum = Field(..., title="接口状态")

class AddApiForm(BaseForm):
    """ 添加接口 """
    project_id: int = Field(..., title="服务id")
    module_id: int = Field(..., title="模块id")
    api_list: List[ApiListModel] = Field(..., title="接口列表")
    api_data_list: List[dict] = Field(None, title="接口数据列表")

    def depends_validate(self):
        api_data_list = [{
            "project_id": self.project_id, "module_id": self.module_id, **api.model_dump()
        } for api in self.api_list]
        self.api_data_list = api_data_list

class ChangeApiForm(GetApiForm):
    """ 修改接口 """
    name: str = Field(..., title="接口名字")
    method: str = Field(..., title="请求方法")
    addr: str = Field(..., title="接口地址")
    desc: Optional[str] = Field(None, title="备注")
    project_id: int = Field(..., title="服务id")
    module_id: int = Field(..., title="模块id")
    up_func: Optional[list] = Field([], title="前置条件")
    down_func: Optional[list] = Field([], title="后置条件")
    extracts: List[ExtractModel] = Field(title="提取信息")
    validates: List[ValidateModel] = Field(title="断言信息")
    headers: List[HeaderModel] = Field(title="头部信息")
    params: List[ParamModel] = Field(title="url参数")
    body_type: ApiBodyTypeEnum = Field(
        ApiBodyTypeEnum.json.value, title="请求体数据类型", description="json/form/text/urlencoded")
    form_data: List[FormDataModel] = Field(title="data-form参数")
    json_data: Union[list, dict] = Field({}, title="json参数")
    form_urlencoded: Union[list, dict] = Field(title="urlencoded参数")
    data_text: Optional[str] = Field(title="文本参数")
    time_out: Optional[int] = Field(title="请求超时时间")
    response: Optional[Union[str, dict, list]] = Field({}, title="接口响应")

    @field_validator('headers')
    def validate_headers(self, value):
        """ 头部信息校验 """
        self.validate_header_format([header.model_dump() for header in value], content_title='头部信息')
        return value

    @field_validator('params')
    def validate_params(self, value):
        """ params信息校验 """
        self.validate_header_format([params.model_dump() for params in value], content_title='url参数')
        return value

    @field_validator('addr')
    def validate_addr(self, value):
        """ 接口地址校验 """
        self.validate_is_true(value.split("?")[0], "接口地址不能为空")
        return value

    @field_validator('extracts')
    def validate_extracts(self, value):
        """ 校验提取数据表达式 """
        self.validate_api_extracts([extract.model_dump() for extract in value])
        return value

    @field_validator('validates')
    def validate_validates(self, value):
        """ 校验断言表达式 """
        self.validate_base_validates([validate.model_dump() for validate in value])
        return value

    def depends_validate(self):
        data_form_value = [data_form.model_dump() for data_form in self.data_form]
        if self.body_type == ApiBodyTypeEnum.form.value:
            self.validate_variable_format(data_form_value, msg_title='form-data')
        return data_form_value

class ChangeLevel(GetApiForm):
    """ 改变接口等级
    id和level
    """
    level: ApiLevelEnum = Field(ApiLevelEnum.LEVEL_2.value,title="接口等级", description="L0、L1、L2")

class DeleteApiForm(GetApiForm):

    @field_validator('id')
    def validate_id(self, value):
        case_name = Api.db.session.query(Case.name).filter(Step.api_id == value).filter(Case.id == Step.case_id).first()
        if case_name:
            raise ValueError(f"用例【{case_name[0]}】已引用此接口，请先解除引用")
        return value
