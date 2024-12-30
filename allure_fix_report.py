# 加载allure_setting中的配置并修改生成的报告文件
import os
import shutil
import subprocess
from sys import platform

from setting import config



def operate_key(aim_file, aim_key, new_key, aim_type):
    """
    :param aim_file: 目标文件
    :param aim_key: 目标关键字
    :param new_key: 需要替换成
    :param aim_type: 需要使用关键字做什么
    """

    # 打开文件
    with open(aim_file, 'r+', encoding="utf-8") as f:
        # 读取当前文件的所有内容
        all_the_lines = f.readlines()
        f.seek(0)
        f.truncate()
        # 循环遍历每一行的内容
        for line in all_the_lines:
            need_write = True
            # 如果目标关键字包含在line中
            if aim_key in line:
                match aim_type:
                    case "replace_key":
                        # 则替换line为new_line
                        f.write(line.replace(aim_key, new_key))   # 替换关键词
                        need_write = False
                    case "replace_line":
                        f.write(line.replace(line, new_key + '\n'))  # 替换关键句
                        need_write = False
                    case "insert_line":
                        f.write(new_key + '\n')  # 在找到的位置插入新标签，并且仅当需要插入时
                        f.write(line)
                        need_write = False
            if len(all_the_lines) and need_write:
                f.write(line)
        # 关闭文件
        f.close()


if __name__ == '__main__':
    aim_index = os.path.join(config.report_path, 'index.html')    # 找到'index.html'所在处
    tag_to_find = '<script src="app.js"></script>'              # 找到"app.js"这一行
    # 修改中文
    aim_settings = os.path.join(config.project_path,config.allure_setting)  # 找到保存的'allure_setting.js'文件

    try:
        shutil.copy2(aim_settings, config.report_path)
    except FileNotFoundError as e:
        print(f"Error occurred during file copy: {e}")
    operate_key(aim_index, tag_to_find, f'<script src={config.allure_setting}></script>', "insert_line")  # 插入 到"app.js" 前面

    # 修改标题
    aim_summary = os.path.join(config.project_path, 'report', 'widgets', 'summary.json')
    operate_key(aim_summary, "Allure Report", config.allure_title, "replace_key")

    # 修改浏览器窗口标题
    operate_key(aim_index, "Allure Report", config.allure_windows_title, "replace_key")


