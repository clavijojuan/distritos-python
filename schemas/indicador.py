from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class Indicador(BaseModel):
    sigla: Optional[str] = Field(None, max_length=20)
    formula: Optional[str] = Field(None,max_length=400)
    nombre: str = Field(max_length=300)
    descripcion: Optional[str] = None
    procedimiento: Optional[str] = None
    cod_proyecto_fk: int
    cod_unidad_fk: int
    peso: float
    cod_padre_fk: Optional[int] = None

class IndicadorUpdate(BaseModel):
    sigla: Optional[str] = None
    formula: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    procedimiento: Optional[str] = None
    cod_proyecto_fk: Optional[int] = None
    cod_unidad_fk: Optional[int] = None
    peso: Optional[float] = None
    cod_padre_fk: Optional[int] = None

class ProyectoDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str

class UnidadDetalle(BaseModel):
    codigo: int
    unidad: str
    descripcion: str
    
class IndicadorResponse(BaseModel):
    codigo:Optional[int]= None
    sigla: Optional[str] = Field(None,max_length=20)
    formula: Optional[str] = Field(None,max_length=400)
    nombre: str = Field(max_length=300)
    descripcion: Optional[str] = None
    procedimiento: Optional[str]
    cod_proyecto_fk: int
    cod_unidad_fk: int
    peso: float
    cod_padre_fk: Optional[int]
    proyecto_detalle: ProyectoDetalle
    unidad_detalle: UnidadDetalle