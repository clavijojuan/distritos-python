from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class UnidadEspacialReferenciaModel(Base):
    
    __tablename__ = "unidad_espacial_referencia_dt"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=9377), index=True)
    cod_proyecto_fk = Column(Integer, ForeignKey('proyecto_distrito_termico.codigo'))
    codigo_elemento = Column(String)

    proyecto_distrito_termicos = relationship("ProyectoDistritoTermico",back_populates="uer")

    IndicadoresValor_dt = relationship("IndicadorValorModel",back_populates="unidad_espacial_sal")
    IndicadoresValor_dt_temporal = relationship("IndicadorValorTemporalModel",back_populates="unidad_espacial_sal_temporal")

        