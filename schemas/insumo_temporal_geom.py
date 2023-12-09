from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any, Dict
from geoalchemy2 import Geometry

class InsumoTemporalGeom(BaseModel):
    campo_calculado: Optional[int] = None
    geom: Any
    cod_insumo_fk: int

class InsumoTemporalGeomUpdate(BaseModel):
    campo_calculado: Optional[int] = None
    geom: Optional[dict] = None
    cod_insumo_fk: Optional[int] = None

class InsumoTemporalGeomQuery(BaseModel):
    campo_calculado: Optional[int] = None
    geom: Optional[dict] = None
    cod_insumo_fk: Optional[int] = None

class InsumoDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str
    
class InsumoTemporalGeomResponse(BaseModel):
    codigo:Optional[int]= None
    campo_calculado: int
    cod_insumo_fk: int
    geom: Optional[dict] = None
    insumos_detalle: InsumoDetalle

    