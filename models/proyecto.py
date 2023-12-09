from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class ProyectoDistritoTermico(Base):
    
    __tablename__ = "proyecto_distrito_termico"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=9377))

    insumos = relationship("InsumoModel",back_populates="proyecto_distrito_termicos")
    uer = relationship("UnidadEspacialReferenciaModel",back_populates="proyecto_distrito_termicos")
    indicadores = relationship("IndicadorModel",back_populates="proyecto_distrito_termicos")

    IndicadoresValor_dt = relationship("IndicadorValorModel",back_populates="proyecto_distrito_termicos_sal")
    IndicadoresValor_dt_temporal = relationship("IndicadorValorTemporalModel",back_populates="proyecto_distrito_termicos_sal_temporal")


    
    