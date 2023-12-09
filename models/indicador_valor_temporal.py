from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, PrimaryKeyConstraint
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

class IndicadorValorTemporalModel(Base):
    
    __tablename__ = "indicador_valor_temporal"

    valor = Column(Float)
    cod_uer_fk = Column(Integer, ForeignKey('unidad_espacial_referencia_dt.codigo'))
    cod_indicador_fk = Column(Integer, ForeignKey('indicador.codigo'))
    cod_proyecto_fk = Column(Integer, ForeignKey('proyecto_distrito_termico.codigo'))
    valor_ponderado = Column(Float)
    cod_ind_padre_fk = Column(Integer)
    cod_escenario_fk = Column(Integer, ForeignKey('escenario.codigo'))
    
    __table_args__ = (
        PrimaryKeyConstraint('valor', 'cod_uer_fk', 'cod_indicador_fk', 'cod_proyecto_fk', 'valor_ponderado', 'cod_ind_padre_fk', 'cod_escenario_fk'),
    )

    proyecto_distrito_termicos_sal_temporal = relationship("ProyectoDistritoTermico",back_populates="IndicadoresValor_dt_temporal")
    unidad_espacial_sal_temporal = relationship("UnidadEspacialReferenciaModel",back_populates="IndicadoresValor_dt_temporal")
    indicador_sal_temporal = relationship("IndicadorModel",back_populates="IndicadoresValor_dt_temporal")
    escenario_sal_temporal = relationship("escenario_model",back_populates="IndicadoresValor_dt_temporal")