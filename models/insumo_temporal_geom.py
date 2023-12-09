from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class InsumoTemporalGeomModel(Base):
    
    __tablename__ = "insumo_temporal_geom"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    campo_calculado = Column(Integer)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=9377), index=True)
    cod_insumo_fk = Column(Integer, ForeignKey('insumo.codigo'))

    insumos_geom_temporal = relationship("InsumoModel",back_populates="insumos_geom")