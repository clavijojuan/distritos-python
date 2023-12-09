from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

class Escenario(BaseModel):
    nombre: str = Field(max_length=150)
    estado: bool
    sincronizado: bool

class EscenarioUpdate(BaseModel):
    nombre: Optional[str] = None
    estado: Optional[bool] = None
    sincronizado: Optional[bool] = None

class EscenarioQuery(BaseModel):
    nombre: Optional[str] = None
    estado: Optional[bool] = None
    sincronizado: Optional[bool] = None

class ProyectoDistritoTermicoDetalle(BaseModel):
    nombre: str
    descripcion: str

class EscenarioIndicadorInsumoDetalle(BaseModel):
    cod_indicador_fk: int
    

class EscenarioResponse(BaseModel):
    codigo: int
    nombre: str = Field(max_length=150)    
    estado: bool
    sincronizado: Optional[bool]
    escenario_insumo_indicador_detalle: List[Dict[str, Any]]
