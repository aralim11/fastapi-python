from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str = "Default Title"
    description: str
    published: Optional[bool] = True