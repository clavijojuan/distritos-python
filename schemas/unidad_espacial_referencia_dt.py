from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any, Dict
from geoalchemy2 import Geometry

class UnidadEspacialReferencia(BaseModel):
    nombre: Optional[str] = Field(None, max_length=300)
    descripcion: Optional[str] = None
    geom: Any
    cod_proyecto_fk: int
    codigo_elemento: Optional[str] = Field(None, max_length=50)

class UnidadEspacialReferenciaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    geom: Optional[dict] = None
    cod_proyecto_fk: Optional[int] = None
    codigo_elemento: Optional[str] = None

class UnidadEspacialReferenciaQuery(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    geom: Optional[dict] = None
    cod_proyecto_fk: Optional[int] = None
    codigo_elemento: Optional[str] = None

class UerDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str
    
class UerResponse(BaseModel):
    codigo:Optional[int]= None
    nombre: Optional[str] = Field(max_length=300)
    descripcion: Optional[str]
    cod_proyecto_fk: int
    codigo_elemento: Optional[str] = Field(max_length=50)
    geom: Optional[Any] = None
    proyecto_detalle: UerDetalle

    