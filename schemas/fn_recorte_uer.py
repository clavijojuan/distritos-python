from pydantic import BaseModel
from typing import List, Dict

class FnRecorteUer(BaseModel):
    codigo_elemento: int
    nombre: str
    descripcion: str
    cod_proyecto_fk: int
    geojson: Dict

    
    


    