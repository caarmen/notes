from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteInput(BaseModel):
    text: str


class Note(NoteInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
