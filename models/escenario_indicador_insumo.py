from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class EscenarioIndicadorInsumoModel(Base):
    
    __tablename__ = "escenario_indicador_insumo"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    cod_insumo_fk = Column(Integer, ForeignKey('insumo.codigo'))
    cod_indicador_fk = Column(Integer, ForeignKey('indicador.codigo'))
    peso = Column(Float)
    cod_escenario_fk = Column(Integer, ForeignKey('escenario.codigo'))

    insumo_dt = relationship("InsumoModel",back_populates="insumos")
    indicador_dt = relationship("IndicadorModel",back_populates="indicadores")
    escenario_dt = relationship("escenario_model", back_populates="escenarios")