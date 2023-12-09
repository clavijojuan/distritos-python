from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.fn_indicador_valor_padre_fija import FnIndicadorValorPadreFijaService
from typing import List, Dict
import json

routerExecIndicadorValorPadre = APIRouter()

@routerExecIndicadorValorPadre.post('/fn-indicador-valor-padre-fija', tags=['funcion'])
async def execute_fn_indicador_valor_padre_fija(codigo_escenario:int = Body()):

    db = SessionLocal()
    service = FnIndicadorValorPadreFijaService(db)
    return service.execute_fn_indicador_valor_padre_fija(
        codigo_escenario
    )