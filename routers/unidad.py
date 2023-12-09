from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.unidad import UnidadService
from schemas.unidad import Unidad, UnidadQuery, UnidadUpdate
from models.unidad import unidad_model
from pydantic import BaseModel

unidad_router = APIRouter()

'''
@unidad_router.get('/unidad',tags=['unidad'], response_model=List[Unidad], status_code=200)
async def get_unidad() -> List[Unidad]:
    try:
        db = SessionLocal()
        result = UnidadService(db).get_unidad()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

@unidad_router.get('/unidad/{codigo}', tags= ['unidad'], response_model=Unidad)
def get_unidad_by_id(codigo: int) -> Unidad:
    try:
        db = SessionLocal()
        result = UnidadService(db).get_unidad_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@unidad_router.get('/unidad', tags= ['unidad'], response_model=List[Unidad])
def get_unidad_by_unidad(unidad:str = Query(None)) -> List[Unidad]:
    try:
        db = SessionLocal()
        result = UnidadService(db).get_by_unidad(unidad)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
  
@unidad_router.post('/unidad', tags=['unidad'], response_model= dict, status_code=201)
def post_unidad(unidad: Unidad) -> dict:
    try:
        db = SessionLocal()
        unidad_creada = UnidadService(db).create_unidad(unidad)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la unidad","unidad creada":unidad_creada['codigo']})
              
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@unidad_router.patch('/unidad/{codigo}', tags=['unidad'], response_model= Unidad, status_code=201)
async def patch_unidad(codigo: int, item_update:UnidadUpdate):
    try:
        db = SessionLocal()
        result = UnidadService(db).get_unidad_by_id(codigo)
        if not result:
            return JSONResponse(status_code=422, content={'message':"No encontrado"})
        proyecto_data = item_update.dict(exclude_unset=True)
        UnidadService(db).patch_unidad(codigo, proyecto_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la unidad"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@unidad_router.delete('/unidad/{codigo}', tags=['unidad'], response_model=dict, status_code=200)
async def delete_unidad(codigo:int) -> dict:
    try:
        db = SessionLocal()
        result = UnidadService(db).get_unidad_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        UnidadService(db).delete_unidad(codigo)
        return JSONResponse(status_code=200, content={"message":"Se ha eliminado la unidad"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))