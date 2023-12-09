from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any, Dict


class SimbologiaIndicador(BaseModel):
    cod_indicador_fk: int
    categoria: List[int]
    minimo: List[float]
    maximo: List[float]
    color_r: List[int] 
    color_g: List[int] 
    color_b: List[int] 
    descripcion: List[str]

class SimbologiaIndicadorUpdate(BaseModel):
    cod_indicador_fk: Optional[int] = None
    categoria: Optional[int] = None
    minimo: Optional[float] = None
    maximo: Optional[float] = None
    color_r: Optional[int] = Field(None, ge=0, le=255)
    color_g: Optional[int] = Field(None, ge=0, le=255)
    color_b: Optional[int] = Field(None, ge=0, le=255)
    descripcion: Optional[str] = None

class IndicadorDetalle(BaseModel):
    codigo: int
    nombre: str
    descripcion: str
    
class SimbologiaIndicadorResponse(BaseModel):
    codigo:Optional[int]= None
    cod_indicador_fk: int
    categoria: int
    minimo: float
    maximo: float
    color_r: int
    color_g: int
    color_b: int
    descripcion: str
    indicador_detalle: IndicadorDetalle
    rgb_expression: Optional[str]
    hex_color: Optional[str]

    @validator("rgb_expression", pre=True, always=True)
    def create_rgb_expression(cls, v, values):
        return f"rgb({values['color_r']}, {values['color_g']}, {values['color_b']})"

    @validator("hex_color", pre=True, always=True)
    def create_hex_color(cls, v, values):
        return "#{:02X}{:02X}{:02X}".format(values['color_r'], values['color_g'], values['color_b'])