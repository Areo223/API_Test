from base.base_models import BaseModel
from exts import db


class Case(BaseModel):
    case_name = db.Column(db.String(50), nullable=False)
