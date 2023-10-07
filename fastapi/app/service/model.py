from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    created_at: datetime
    updated_at: datetime
