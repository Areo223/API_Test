# 本文件是项目的配置文件
import os

from setuptools.config.expand import StaticModule

class Config:
    # 项目路径
    project_path = os.path.dirname(os.path.abspath(__file__))

    # Allure安装路径
    allure_install_path = os.path.join(project_path, "allure")

    # Allure程序路径
    allure_bin_path = os.path.join(project_path, "allure/bin/")

    # 临时文件路径
    temp_path = os.path.join(project_path, "temp")

    # URL
    base_url = "http://localhost:8080/diary"

    #allure配置文件
    allure_setting="allure_setting.js"

    #allure修改文件
    allure_fix_report="allure_fix_report.py"

    # 测试报告路径
    report_path = os.path.join(project_path, 'report')
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    # allure修改内容
    # 修改标题
    allure_title="自动化Api测试框架"
    # 修改窗口标题
    allure_windows_title = "自动化Api测试框架"




config = Config()

if __name__ == "__main__":
    pass