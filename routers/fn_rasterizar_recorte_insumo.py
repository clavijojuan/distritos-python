from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.fn_rasterizar_recorte_insumo import FnRasterizarRecorteInsumoService
from typing import List, Dict
import json

routerExecRasterizar = APIRouter()

@routerExecRasterizar.post('/fn-rasterizar-recorte', tags=['funcion'])
#async def execute_fn_recorte_uer(fn_recorte_uer_data: FnRecorteUer, db: Session = Depends(SessionLocal)):
async def execute_fn_rasterizar_recorte(codigo_proyecto:int = Body(), codigo_insumo:int = Body()):

    db = SessionLocal()
    service = FnRasterizarRecorteInsumoService(db)
    return service.execute_fn_rasterizar_recorte_insumo(
        codigo_proyecto,
        codigo_insumo
    )
