from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
#######################################################
# 
# color.py
# Python implementation of the Class color
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):      11-Feb-2020 11(FTSProtocolObject):08(FTSProtocolObject):07 AM
# Original author: Corvo
# 
#######################################################
from FreeTAKServer.model.FTSModelVariables.ColorVariables import ColorVariables as vars

class Color(FTSProtocolObject):
    def __init__(self):
        self.argb = None

    @staticmethod
    def drop_point(ARGB = vars.drop_point().ARGB):
        color = Color()
        color.setargb(ARGB)
        return color

    # argb getter 
    def getargb(self): 
        return self.argb 

    # argb setter 
    def setargb(self, argb=0):  
        self.argb=argb 
