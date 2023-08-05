#######################################################
# 
# Link.py
# Python implementation of the Class Link
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 9:41:33 PM
# Original author: natha
# 
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship


class Link(Base):
# default constructor  def __init__(self):  
    __tablename__ = "Link"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="link")
    #PrimaryKey = Column(ForeignKey('detail.uid'), primary_key=True)
    # Internet Media type of the referenced object.  If the link is to a CoT event,
    # the mime attribute is optional and its type may be application/xml or text/xml
    # as described in RFC 3023, "XML Media Types", or the unregistered type,
    # application/cot+xml.  If the link is to an arbitrary resource, the mime
    # attribute is required and and appropriate Internet media type must be specified.
    #  Registered media types are managed by the IANA and are listed at http://www.
    # iana.org/assignments/media-types/.
    mime = Column(String(100))
    parent_callsign = Column(String(100))
    production_time = Column(String(100))
    # The type of relationship (e.g, subject, object, indirect object) that this link
    # describes.  This is a hierarchy much like the event type field.
    relation = Column(String(100))
    # Remarks associated with this link.
    remarks = Column(String(100))
    # The CoT type of the referenced object.  This is included because it is
    # generally the key item needed in a tasking.
    type = Column(String(100))
    uid = Column(String(100))
    # If present, this is a URL through which the linked object can be retrieved.
    # If the URL is missing, then the object should be a periodic message (e.g., blue
    # force track) that can be read from a CoT stream.
    url = Column(String(100))
    # Version tag for this sub schema.  Neccessary to ensure upward compatibility
    # with future revisions.
    version = Column(String(100))