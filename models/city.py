#!/usr/bin/python
"""class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representing city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializing city."""
        super().__init__(*args, **kwargs)
