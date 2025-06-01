from database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    published = Column(Integer, default=1)  # 1 for True, 0 for False
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)