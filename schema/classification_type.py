from pydantic import BaseModel
from type import Type

class ClassificationType(BaseModel):
    selected_type: Type