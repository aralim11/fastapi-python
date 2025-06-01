from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    description: str
    published: Optional[bool] = True