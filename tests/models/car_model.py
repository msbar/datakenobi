from sqlalchemy import BIGINT, INTEGER, VARCHAR, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "Car"
    __table_args__ = {"schema": "main"}

    id = Column(BIGINT, primary_key=True)
    make = Column(VARCHAR(50))
    model = Column(VARCHAR(50))
    year = Column(INTEGER)
