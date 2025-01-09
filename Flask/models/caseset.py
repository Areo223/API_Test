from sqlalchemy.orm import relationship

from Flask.exts import db
from Flask.secondary.secondary import caseset_case
from base.base_models import BaseModel


class CaseSet(BaseModel):
    caseset_name = db.Column(db.String(50), nullable=False)

    case=relationship("Case",secondary=caseset_case,backref="CaseSet")
