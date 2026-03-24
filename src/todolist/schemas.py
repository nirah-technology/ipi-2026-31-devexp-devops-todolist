from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Status(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    status: Status