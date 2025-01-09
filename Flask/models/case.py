from Flask.exts import db
from base.base_models import BaseModel


class Case(BaseModel):
    case_name = db.Column(db.String(50), nullable=False)
