from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

class Unidad(BaseModel):
    codigo:Optional[int]= None
    unidad: str = Field(max_length=150)
    descripcion: str

class UnidadUpdate(BaseModel):
    unidad: Optional[str] = None
    descripcion: Optional[str] = None

class UnidadQuery(BaseModel):
    unidad: Optional[str] = None
    descripcion: Optional[str] = None
    