from Flask.exts import db
from base.base_models import StatusFiledModel


class User(StatusFiledModel):

    account = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
