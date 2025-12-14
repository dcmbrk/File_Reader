from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from connection.db import Model
from sqlalchemy.types import JSON

class Rules(Model):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(32))
    regex: Mapped[dict] = mapped_column(JSON)

    def __repr__(self):
        return f'Rule:({self.id} "{self.type}")'
    
class Data(Model):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"))
    value: Mapped[dict] = mapped_column(JSON)

    def __repr__(self):
        return f':({self.id} "{self.name}")'
