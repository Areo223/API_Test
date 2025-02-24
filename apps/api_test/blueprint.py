from ..base_view import Blueprint

api_test = Blueprint("api_test", __name__)

from .views import api
