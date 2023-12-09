from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class unidad_model(Base):
    
    __tablename__ = "unidad"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    unidad = Column(String)
    descripcion = Column(String)
    
    unidades = relationship("IndicadorModel",back_populates="unidades_dt")
