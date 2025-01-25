from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.base_model import BaseModel


class Config(BaseModel):
    """ 配置表 """

    __tablename__ = "config_config"
    __table_args__ = {"comment": "配置表"}

    type: Mapped[int] = mapped_column(Integer(), nullable=False, index=True, comment="配置类型")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, unique=True, comment="配置名")
    value: Mapped[str] = mapped_column(Text(), comment="配置值")
    desc: Mapped[str] = mapped_column(Text(), nullable=True, comment="描述")