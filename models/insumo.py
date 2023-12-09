from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class InsumoModel(Base):
    
    __tablename__ = "insumo"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    cod_proyecto_fk = Column(Integer, ForeignKey('proyecto_distrito_termico.codigo'))
    campo_calculado = Column(String)
    sigla = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=9377), index=True)

    proyecto_distrito_termicos = relationship("ProyectoDistritoTermico",back_populates="insumos")
    insumos = relationship("EscenarioIndicadorInsumoModel",back_populates="insumo_dt")
    insumos_geom = relationship("InsumoTemporalGeomModel",back_populates="insumos_geom_temporal")







