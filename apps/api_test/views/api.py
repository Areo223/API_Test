from threading import Thread

from flask import current_app as app

from ..blueprint import api_test
from apps.api_test.forms.api import ApiListForm, ChangeStatusForm, GetApiForm, AddApiForm, ChangeApiForm, DeleteApiForm, \
    RunApiForm
from ..model_factory import ApiMsg as Api,ApiReport as Report
from apps.config.models.run_env import RunEnv


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


@api_test.login_delete("/api")
def api_delete_api():
    """
    删除接口
    """
    form = DeleteApiForm()
    Api.delete_by_id(form.id)
    return app.restful.delete_success()


@api_test.login_put("/api")
def api_change_api():
    form = ChangeApiForm()
    form.api.model_update(form.model_dump())
    return app.restful.change_success()

@api_test.login_post("/api/status")
def api_status():
    form = ChangeStatusForm()
    Api.query.filter_by(Api.id==form.id).update({"status":form.status.value})
    return app.restful.change_success()

@api_test.login_put("/api/level")
def api_change_api_level():
    form = ChangeApiForm()
    form.api.model_update(form.model_dump())
    return app.restful.change_success()


@api_test.login_get("/api")
def api_get_api():
    form = GetApiForm()
    return app.restful.get_success(form.api.to_dict())


@api_test.login_post("/api/run")
def api_run_api():
    """ 运行接口 """
    form = RunApiForm()
    batch_id = Report.get_batch_id()
    summary = Report.get_summary_template()
    # 遍历环境，生成报告
    # 开发环境,测试环境,生产环境,uat环境
    for env_code in form.env_list:
        env = RunEnv.get_data_by_id_or_code(env_code)
        summary["env"]["code"], summary["env"]["name"] = env.code, env.name
        report = Report.get_new_report(
            batch_id=batch_id,
            trigger_id=form.id_list,
            name=form.api_name,
            run_type="api",
            env=env_code,
            project_id=form.project_id,
            summary=summary
        )

        # 新起线程运行接口
        Thread(
            target=RunApi(
                api_id_list=form.run_api_id_list,
                report_id=report.id,
                env_code=env_code,
                env_name=env.name
            ).parse_and_run
        ).start()
    return app.restful.trigger_success({"batch_id": batch_id})
