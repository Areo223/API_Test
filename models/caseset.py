from sqlalchemy.orm import relationship

from base.base_models import BaseModel
from exts import db
from secondary.secondary import caseset_case


class CaseSet(BaseModel):
    caseset_name = db.Column(db.String(50), nullable=False)

    case=relationship("Case",secondary=caseset_case,backref="CaseSet")
