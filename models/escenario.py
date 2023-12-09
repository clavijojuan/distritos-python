from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, Boolean
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class escenario_model(Base):
    
    __tablename__ = "escenario"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    estado = Column(Boolean)
    sincronizado = Column(Boolean)
    
    escenarios = relationship("EscenarioIndicadorInsumoModel",back_populates="escenario_dt")

    IndicadoresValor_dt = relationship("IndicadorValorModel",back_populates="escenario_sal")
    IndicadoresValor_dt_temporal = relationship("IndicadorValorTemporalModel",back_populates="escenario_sal_temporal")