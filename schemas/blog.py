from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class Blog(BaseModel):
    title: str
    description: str
    published: Optional[bool] = True
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)