#######################################################
# 
# Root.py
# Python implementation of the Class Root
# Generated by Enterprise Architect
# Created on:      21-Sep-2020 10:28:05 PM
# Original author: natha
# 
#######################################################
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer

Base = declarative_base()

class Root:
    uid = Column(String(100))