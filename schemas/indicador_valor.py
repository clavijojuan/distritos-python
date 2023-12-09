from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class IndicadorValor(BaseModel):
    codigo: Optional[int]
    valor: float 
    cod_uer_fk: int
    cod_indicador_fk: int
    cod_proyecto_fk: int
    valor_ponderado: float
    cod_ind_padre_fk: Optional[int] = None
    cod_escenario_fk: int

class UerDetalle(BaseModel):
    codigo: int
    geom: Any

class IndicadorDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str

class ProyectoDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str

class EscenarioDetalle(BaseModel):
    codigo: int
    nombre: str
    estado: bool
    sincronizado: bool
    
class IndicadorValorResponse(BaseModel):
    codigo:Optional[int]= None
    valor: float
    cod_uer_fk: int
    cod_indicador_fk: int
    cod_proyecto_fk: int
    valor_ponderado: float
    cod_ind_padre_fk: Optional[int]
    cod_escenario_fk: int
    uer_detalle: UerDetalle
    indicador_detalle: IndicadorDetalle
    proyecto_detalle: ProyectoDetalle
    escenario_detalle: EscenarioDetalle