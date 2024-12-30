# 本文件是程序的主入口
import os
from setting import config

os.system(f"pytest -s -q --alluredir={config.temp_path}")
# 生成测试报告
os.system(f"allure generate {config.temp_path} --clean -o {config.report_path}")
# 修改报告
os.system(f"python {os.path.join(config.project_path, config.allure_fix_report)}")
# 打开生成的报告
os.system(f"allure open {config.report_path}")
