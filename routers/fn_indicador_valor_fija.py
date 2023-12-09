from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.fn_indicador_valor_fija import FnIndicadorValorFijaService
from typing import List, Dict
import json

routerExecIndicadorValor = APIRouter()

@routerExecIndicadorValor.post('/fn-indicador-valor-fija', tags=['funcion'])
async def execute_fn_indicador_valor_fija(codigo_escenario:int = Body()):

    db = SessionLocal()
    service = FnIndicadorValorFijaService(db)
    return service.execute_fn_indicador_valor_fija(
        codigo_escenario
    )
