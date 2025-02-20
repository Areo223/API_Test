from pydantic import Field

from apps.system.models.user import User
from config import _admin_default_password
from apps.base_form import BaseForm


class LoginForm(BaseForm):
    account:str = Field(title="账号",min_length=6,max_length=16)
    password:str = Field(title="密码",min_length=6,max_length=16)

    def depends_validate(self):
        if self.account == "admin" and self.password == _admin_default_password:
            user = User.get_first(account=self.account)
        else:
            user = self.validate_data_is_exist(msg="账号不存在",account=self.account)
            self.validate_is_true(user.status != 0,msg="账号已被禁用")
            self.validate_is_true(user.verify_password(self.password),msg="账号或密码错误")
        setattr(self,"user",user)