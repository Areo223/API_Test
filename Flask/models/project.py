from sqlalchemy.orm import relationship

from Flask.exts import db
from Flask.secondary.secondary import project_module, project_user, project_caseset
from base.base_models import BaseModel


class Project(BaseModel):
    project_name = db.Column(db.String(50), nullable=False)
    # 服务根路径
    project_url = db.Column(db.String(50), nullable=False)
    # 接口文档地址
    swagger = db.Column(db.String(50), nullable=True)

    model = relationship('Model',secondary=project_module,backref='project',lazy='dynamic')
    user = relationship("User",secondary=project_user,backref="project",lazy='dynamic')
    caseset = relationship("CaseSet",secondary=project_caseset,backref="project",lazy='dynamic')

