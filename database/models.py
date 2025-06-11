from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    survival_time: int = Field(..., ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)