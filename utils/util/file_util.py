import os

from config import _basedir as basedir
# 模块路径
LOG_ADDRESS = os.path.abspath(os.path.join(basedir, ".." + r"/logs/"))  # 日志路径