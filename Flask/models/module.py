from sqlalchemy.orm import relationship

from Flask.exts import db
from Flask.secondary.secondary import module_api
from base.base_models import BaseModel


class Module(BaseModel):

    module_name = db.Column(db.String(50), nullable=False)

    api = relationship("Api", secondary=module_api, backref="Module",lazy="dynamic")
