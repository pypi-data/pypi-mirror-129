#######################################################
# 
# VideoStreamTableController.py
# Python implementation of the Class VideoStreamTableController
# Generated by Enterprise Architect
# Created on:      24-Sep-2020 8:19:58 PM
# Original author: natha
# 
#######################################################
from FreeTAKServer.controllers.DatabaseControllers.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.VideoStream import VideoStream

class VideoStreamTableController(TableController):

    def __init__(self):
        self.table = VideoStream