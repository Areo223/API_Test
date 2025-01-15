
from sqlalchemy.orm import Mapped, mapped_column

from apps.base_model import BaseProject
from apps.enums import ProjectLastPullStatusEnum


class ApiProject(BaseProject):
    __abstract__ = False
    __table_name__ = 'api_test_project'
    __table_args__ = {'comment': '接口测试项目信息表'}

    last_pull_status:Mapped[ProjectLastPullStatusEnum] = mapped_column(default=ProjectLastPullStatusEnum.NOT_PULL,comment="最后一次拉取状态,2成功,1未拉取,0失败")

    def last_pull_fail(self):
        self.model_update({"last_pull_status":ProjectLastPullStatusEnum.FAIL})

    def last_pull_success(self):
        self.model_update({"last_pull_status":ProjectLastPullStatusEnum.SUCCESS})