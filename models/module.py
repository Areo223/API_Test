from sqlalchemy.orm import relationship

from base.base_models import BaseModel
from exts import db
from secondary.secondary import module_api


class Module(BaseModel):

    module_name = db.Column(db.String(50), nullable=False)

    api = relationship("Api", secondary=module_api, backref="Module",lazy="dynamic")
