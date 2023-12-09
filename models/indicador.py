from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class IndicadorModel(Base):
    
    __tablename__ = "indicador"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    sigla = Column(String)
    formula = Column(String)
    nombre = Column(String)
    descripcion = Column(String)
    procedimiento = Column(String)
    #cod_proyecto_fk = Column(Integer)
    cod_proyecto_fk = Column(Integer, ForeignKey('proyecto_distrito_termico.codigo'))
    cod_unidad_fk = Column(Integer, ForeignKey('unidad.codigo'))
    peso = Column(Float)
    cod_padre_fk = Column(Integer)
    

    proyecto_distrito_termicos = relationship("ProyectoDistritoTermico",back_populates="indicadores")
    unidades_dt = relationship("unidad_model",back_populates="unidades")
    indicadores = relationship("EscenarioIndicadorInsumoModel",back_populates="indicador_dt")
    indicadores_s = relationship("SimbologiaIndicadorModel",back_populates="indicador_dt")

    IndicadoresValor_dt = relationship("IndicadorValorModel",back_populates="indicador_sal")
    IndicadoresValor_dt_temporal = relationship("IndicadorValorTemporalModel",back_populates="indicador_sal_temporal")