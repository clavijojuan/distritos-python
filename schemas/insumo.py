from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class Insumo(BaseModel):
    codigo:Optional[int]= None
    nombre: str = Field(max_length=250)
    descripcion: Optional[str] = None
    cod_proyecto_fk: int
    campo_calculado: str = Field(max_length=100)
    sigla: Optional[str] = Field(None, max_length=20)
    geom: Any

class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cod_proyecto_fk: Optional[int] = None
    campo_calculado: Optional[str] = None
    sigla: Optional[str] = None

class ProyectoDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str
    
class InsumoResponse(BaseModel):
    codigo:Optional[int]= None
    nombre: str = Field(max_length=250)
    descripcion: str
    cod_proyecto_fk: int
    campo_calculado: str = Field(max_length=100)
    sigla: str = Field(max_length=20)
    proyecto_detalle: ProyectoDetalle





    