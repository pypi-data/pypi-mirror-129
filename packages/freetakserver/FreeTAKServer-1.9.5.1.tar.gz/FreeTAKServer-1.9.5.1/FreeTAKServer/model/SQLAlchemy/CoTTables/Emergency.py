#######################################################
# 
# emergency.py
# Python implementation of the Class emergency
# Generated by Enterprise Architect
# Created on:      28-Sep-2020 10:48:15 PM
# Original author: natha
# 
#######################################################
from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Emergency(Base):
    __tablename__ = "Emergency"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="emergency")
    Alert = Column(String(100))
    # if true the emergency beacon is canceled
    cancel = Column(String(100))
    # default constructor  def __init__(self):
    type = Column(String(100))