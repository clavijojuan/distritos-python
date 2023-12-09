from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class SimbologiaIndicadorModel(Base):
    
    __tablename__ = "simbologia_indicador"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    cod_indicador_fk = Column(Integer, ForeignKey('indicador.codigo'))
    categoria = Column(Integer)
    minimo = Column(Float)
    maximo = Column(Float)
    color_r = Column(Integer)
    color_g = Column(Integer)
    color_b = Column(Integer)
    descripcion = Column(String)

    indicador_dt = relationship("IndicadorModel",back_populates="indicadores_s")

