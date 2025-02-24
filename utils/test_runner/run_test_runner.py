# from apps.api_test.model_factory import ApiMsg,ApiReport,ApiProject,ApiStep,ApiCase,ApiCaseSuite,ApiProjectEnv,ApiReportCase,ApiReportStep
# from apps.config.model_factory import Config
#
# class RunTestRunner:
#     """
#     测试运行器类，用于执行测试并管理测试数据和环境。
#
#     属性:
#         env_code (str): 环境代码。
#         env_name (str): 环境名称，用于发送即时通讯。
#         extend (dict): 扩展字典。
#         report_id (int): 报告ID。
#         run_type (str): 运行类型，默认为 "api"。
#         task_dict (dict): 任务字典。
#         time_out (int): 超时时间，默认为 60 秒。
#         wait_time_out (int): 等待超时时间，默认为 5 秒。
#         count_step (int): 步骤计数器。
#         api_set (set): API 集合。
#         element_set (set): 元素集合。
#         parsed_project_dict (dict): 解析后的项目字典。
#         parsed_case_dict (dict): 解析后的用例字典。
#         parsed_api_dict (dict): 解析后的 API 字典。
#         parsed_element_dict (dict): 解析后的元素字典。
#         run_env (object): 运行环境对象。
#         report (object): 报告对象。
#         response_time_level (dict): 响应时间级别。
#         api_model (object): API 模型对象。
#         element_model (object): 元素模型对象。
#         project_model (object): 项目模型对象。
#         project_env_model (object): 项目环境模型对象。
#         suite_model (object): 套件模型对象。
#         case_model (object): 用例模型对象。
#         step_model (object): 步骤模型对象。
#         report_model (object): 报告模型对象。
#         report_case_model (object): 报告用例模型对象。
#         report_step_model (object): 报告步骤模型对象。
#         front_report_addr (str): 前端报告地址。
#         run_test_data (dict): 运行测试数据。
#
#     方法:
#         __init__(self, report_id=None, env_code=None, env_name=None, run_type="api", extend={}, task_dict={}):
#             初始化测试运行器实例。
#
#         init_parsed_data(self):
#             初始化解析后的数据。
#
#         get_report_addr(self):
#             获取报告前端地址。
#
#         get_format_project(self, project_id):
#             从已解析的服务字典中获取指定 ID 的服务，如果没有，则解析后放入字典。
#
#         get_format_case(self, case_id):
#             从已解析的用例字典中获取指定 ID 的用例，如果没有，则解析后放入字典。
#
#         get_format_element(self, element_id):
#             从已解析的元素字典中获取指定 ID 的元素，如果没有，则解析后放入字典。
#
#         get_format_api(self, project, api_id=None, api_obj=None):
#             从已解析的接口字典中获取指定 ID 的接口，如果没有，则解析后放入字典。
#     """
#
#     def __init__(
#             self, report_id=None, env_code=None, env_name=None, run_type="api", extend={}, task_dict={}):
#         """
#         初始化测试运行器实例。
#
#         参数:
#             report_id (int): 报告ID。
#             env_code (str): 环境代码。
#             env_name (str): 环境名称。
#             run_type (str): 运行类型，默认为 "api"。
#             extend (dict): 扩展字典。
#             task_dict (dict): 任务字典。
#         """
#         self.env_code = env_code  # 运行环境id
#         self.env_name = env_name  # 运行环境名，用于发送即时通讯
#         self.extend = extend
#         self.report_id = report_id
#         self.run_type = run_type
#         self.task_dict = task_dict
#
#         self.time_out = 60
#         self.wait_time_out = 5
#         self.count_step = 0
#         # set()为创建集合
#         self.api_set = set()
#         self.element_set = set()
#         self.parsed_project_dict = {}
#         self.parsed_case_dict = {}
#         self.parsed_api_dict = {}
#         self.parsed_element_dict = {}
#         self.run_env = None
#         self.report = None
#         self.response_time_level = {"slow": 0, "very_slow": 0}
#         self.api_model = ApiMsg
#         self.element_model = None
#         self.project_model = ApiProject
#         self.project_env_model = ApiProjectEnv
#         self.suite_model = ApiCaseSuite
#         self.case_model = ApiCase
#         self.step_model = ApiStep
#         self.report_model = ApiReport
#         self.report_case_model = ApiReportCase
#         self.report_step_model = ApiReportStep
#         self.time_out = Config.get_request_time_out()
#         self.response_time_level = Config.get_response_time_level()
#         self.front_report_addr = f'{Config.get_report_host()}{Config.get_api_report_addr()}'
#         # testRunner需要的数据格式
#         self.run_test_data = {
#             "is_async": 0,
#             "run_type": self.run_type,
#             "report_id": self.report_id,
#             "report_model": self.report_model,
#             "report_case_model": self.report_case_model,
#             "report_step_model": self.report_step_model,
#             "response_time_level": self.response_time_level,
#             "pause_step_time_out": Config.get_pause_step_time_out(),
#             "project_mapping": {
#                 "functions": {},
#                 "variables": {},
#             },
#             "report_case_list": [],  # 用例
#         }
#
#         self.init_parsed_data()
#
#     def init_parsed_data(self):
#         """
#         初始化解析后的数据。
#         """
#         self.parsed_project_dict = {}
#         self.parsed_case_dict = {}
#         self.parsed_api_dict = {}
#         self.parsed_element_dict = {}
#         self.run_env = None
#
