from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class EscenarioIndicadorInsumo(BaseModel):
    cod_insumo_fk: List[int]
    cod_indicador_fk: int
    peso: List[float]
    cod_escenario_fk: int

class EscenarioIndicadorInsumoUpdate(BaseModel):
    cod_insumo_fk: Optional[int] = None
    cod_indicador_fk: Optional[int] = None
    peso: Optional[float] = None
    cod_escenario_fk: Optional[int] = None
    
class InsumoDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str

class IndicadorDetalle(BaseModel):
    codigo: int
    nombre: str

class EscenarioDetalle(BaseModel):
    codigo: int
    nombre: str
    estado: bool
    sincronizado: bool
    
class EscenarioIndicadorInsumoResponse(BaseModel):
    codigo:Optional[int]= None
    cod_insumo_fk: Optional[int] = None
    cod_indicador_fk: Optional[int] = None
    peso: Optional[float] = None
    cod_escenario_fk: Optional[int] = None
    insumo_detalle: InsumoDetalle
    indicador_detalle: IndicadorDetalle
    escenario_detalle: EscenarioDetalle
