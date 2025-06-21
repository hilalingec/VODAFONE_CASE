from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database import Base

import warnings
warnings.filterwarnings('ignore') 


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    date = Column(TIMESTAMP, default=func.now(), onupdate=func.now())