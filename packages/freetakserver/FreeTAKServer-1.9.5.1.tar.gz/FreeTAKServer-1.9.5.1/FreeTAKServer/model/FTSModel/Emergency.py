from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
#######################################################
# 
# Emergency.py
# Python implementation of the Class Emergency
# Generated by Enterprise Architect
# Created on:      13-Apr-2020 4:40:22 PM
# Original author: Corvo
# 
#######################################################
from FreeTAKServer.model.FTSModelVariables.EmergencyVariables import EmergencyVariables as vars

class Emergency(FTSProtocolObject):
    """An Emergency beacon the is continually send to all the connected clients until
    deactivated from the original creator
    """
    def __init__(self):  
        self.type = None
        self.alert = None
    # if true the Emergency beacon is canceled
        self.cancel = None
        self.INTAG = None

    @staticmethod
    def emergency_on(INTAG = vars.emergency_on().INTAG, TYPE = vars.emergency_on().TYPE, ALERT = vars.emergency_on().ALERT, CANCEL = vars.emergency_on().CANCEL):
        emergency = Emergency()
        emergency.settype(TYPE)
        emergency.setAlert(ALERT)
        emergency.setcancel(CANCEL)
        emergency.setINTAG(INTAG)
        return emergency

    @staticmethod
    def emergency_off(CANCEL = vars.emergency_off().CANCEL, INTAG = vars.emergency_off().INTAG):
        emergency = Emergency()
        emergency.setcancel(CANCEL)
        emergency.setINTAG(INTAG)
        return emergency

    def settype(self, type=None):
        self.type = type
    
    def gettype(self):
        return self.type

    def setAlert(self, alert=None):
        self.alert = alert

    def getAlert(self):
        return self.alert

    def setcancel(self, cancel=None):
        self.cancel = cancel

    def getcancel(self):
        return self.cancel

    def setINTAG(self, INTAG=None):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
