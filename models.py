from sqlalchemy import Column, Integer, String

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    url = Column(String)
    method = Column(String)
    cron_expression = Column(String)
    description = Column(String)
