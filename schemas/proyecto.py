from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any, Dict
from geoalchemy2 import Geometry

class Proyecto(BaseModel):
    nombre: str = Field(max_length=300)
    descripcion: str
    geom: Any

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    geom: Optional[dict] = None

class ProyectoQuery(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    geom: Optional[dict] = None