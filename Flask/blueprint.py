from flask import Blueprint

api_test = Blueprint('apiTest', __name__)

# 加载视图
from .views import api_view
