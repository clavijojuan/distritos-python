from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.fn_recorte_uer import FnRecorteUer
from services.fn_recorte_uer import FnRecorteUerService
from typing import List, Dict
import json
from shapely.geometry import shape

routerExec = APIRouter()

@routerExec.post('/fn-recorte-uer', tags=['funcion'])
#async def execute_fn_recorte_uer(fn_recorte_uer_data: FnRecorteUer, db: Session = Depends(SessionLocal)):
async def execute_fn_recorte_uer(codigo_elemento:List[int] = Body(), nombre: List[str] = Body(), descripcion: List[str] = Body(), cod_proyecto_fk: int = Body(), geojson: Dict = Body()):

    db = SessionLocal()
    geojson_str = json.dumps(geojson)
    #print(geojson_str)
    service = FnRecorteUerService(db)
    return service.execute_fn_recorte_uer(
        codigo_elemento,
        nombre,
        descripcion,
        cod_proyecto_fk,
        geojson_str
    )
