# 获取测试环境
import os
from sys import platform

from allure_fix_report import operate_key
from setting import config

aim_environment = os.path.join(config.project_path, 'environment.properties')
copy_environment = os.path.join(config.project_path, 'temp', 'html', 'environment.properties')
os.system(f"copy {aim_environment} {copy_environment}")

environment_info = {
    "systemVersion": platform.system().lower(),
    "pythonVersion":os.system("python --version"),
    "allureVersion":os.system("allure --version"),
    "author": os.system("git config user.name"),
    "projectLocation": os.getcwd()
}
for key in environment_info:
    operate_key(copy_environment, key, f"{key} = {environment_info[key]}", "replace_line")