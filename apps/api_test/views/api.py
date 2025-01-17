from flask import current_app as app

from apps.api_test.blueprint import api_test
from apps.api_test.forms.api import ApiListForm, ChangeStatusForm, GetApiForm, AddApiForm, ChangeApiForm, DeleteApiForm
from ..model_factory import ApiMsg as Api

@api_test.login_get("/api/list")
def api_list():
    form = ApiListForm()
    if form.detail:
        get_filed = [
            Api.id, Api.name, Api.project_id,
            Api.module_id, Api.addr, Api.method,
            Api.use_count, Api.level,
            Api.status, Api.create_user
        ]
    else:
        get_filed = [
            Api.id, Api.name]

    return app.restful.get_success(Api.make_pagination(form,get_filed))

@api_test.login_post("/api/status")
def api_status():
    form = ChangeStatusForm()
    Api.query.filter_by(Api.id==form.id).update({"status":form.status.value})
    return app.restful.change_success()

@api_test.login_get("/api")
def api_get_api():
    form = GetApiForm()
    return app.restful.get_success(form.api.to_dict())

@api_test.login_post("/api")
def api_add_api():
    form = AddApiForm()
    # 如果是新增一个
    if len(form.api_list) == 1:
        api = Api.model_create_and_get(form.api_data_list[0])
        return app.restful.add_success(api.to_dict())
    # 如果是批量新增
    Api.model_batch_create(form.api_data_list)
    return app.restful.post_success()

@api_test.login_put("/api")
def api_change_api():
    form = ChangeApiForm()
    form.api.model_update(form.model_dump())
    return app.restful.change_success()

@api_test.login_put("/api/level")
def api_change_api_level():
    form = ChangeApiForm()
    form.api.model_update(form.model_dump())
    return app.restful.change_success()

@api_test.login_delete("/api")
def api_delete_api():
    """
    删除接口
    """
    form = DeleteApiForm()
    Api.delete_by_id(form.id)
    return app.restful.delete_success()


