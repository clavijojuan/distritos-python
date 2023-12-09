from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class IndicadorValorModel(Base):
    
    __tablename__ = "indicador_valor"

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float)
    cod_uer_fk = Column(Integer, ForeignKey('unidad_espacial_referencia_dt.codigo'))
    cod_indicador_fk = Column(Integer, ForeignKey('indicador.codigo'))
    cod_proyecto_fk = Column(Integer, ForeignKey('proyecto_distrito_termico.codigo'))
    valor_ponderado = Column(Float)
    cod_ind_padre_fk = Column(Integer)
    cod_escenario_fk = Column(Integer, ForeignKey('escenario.codigo'))
    
    

    proyecto_distrito_termicos_sal = relationship("ProyectoDistritoTermico",back_populates="IndicadoresValor_dt")
    unidad_espacial_sal = relationship("UnidadEspacialReferenciaModel",back_populates="IndicadoresValor_dt")
    indicador_sal = relationship("IndicadorModel",back_populates="IndicadoresValor_dt")
    escenario_sal = relationship("escenario_model",back_populates="IndicadoresValor_dt")
    

    