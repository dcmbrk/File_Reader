from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from connection.db import Model
from sqlalchemy.types import JSON
import datetime

class Document(Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(Text) 
    
    data: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        server_default=func.now() 
    )

    def __repr__(self) -> str:
        return f'<Document(id={self.id}, name="{self.name}")>'