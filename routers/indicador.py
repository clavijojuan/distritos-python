from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.indicador import IndicadorService
from schemas.indicador import Indicador, IndicadorResponse, IndicadorUpdate
from models.indicador import IndicadorModel


indicador_router = APIRouter()

'''
@indicador_router.get('/indicador',tags=['indicador'], response_model=List[Indicador], status_code=200)
async def get_indicador() -> List[Indicador]:
    try:
        db = SessionLocal()
        result = IndicadorService(db).get_indicador()
        result_dict_list = []
        for proyecto in result:
            proyecto_detalle = {
                "codigo": proyecto.proyecto_distrito_termicos.codigo,
                "nombre": proyecto.proyecto_distrito_termicos.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos.descripcion
            }
            unidad_detalle = {
                "codigo": proyecto.unidades_dt.codigo,
                "unidad": proyecto.unidades_dt.unidad,
                "descripcion": proyecto.unidades_dt.descripcion 
            }   
            indicador_response = IndicadorResponse(
                codigo=proyecto.codigo,
                sigla=proyecto.sigla,
                formula=proyecto.formula,
                nombre=proyecto.nombre,
                descripcion=proyecto.descripcion,
                procedimiento=proyecto.procedimiento,
                cod_proyecto_fk=proyecto.cod_proyecto_fk,
                cod_unidad_fk=proyecto.cod_unidad_fk,
                peso=proyecto.peso,
                cod_padre_fk=proyecto.cod_padre_fk,
                proyecto_detalle=proyecto_detalle,
                unidad_detalle=unidad_detalle
                )
            result_dict_list.append(indicador_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

@indicador_router.get('/indicador/{codigo}', tags= ['indicador'], response_model=Indicador)
def get_indicador_by_id(codigo: int) -> Indicador:
    try:
        db = SessionLocal()
        result = IndicadorService(db).get_indicador_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        
        proyecto_detalle = {
            "codigo": result.proyecto_distrito_termicos.codigo,
            "nombre": result.proyecto_distrito_termicos.nombre,
            "descripcion": result.proyecto_distrito_termicos.descripcion
        }
        unidad_detalle = {
            "codigo": result.unidades_dt.codigo,
            "unidad": result.unidades_dt.unidad,
            "descripcion": result.unidades_dt.descripcion 
        }
        indicador_response = IndicadorResponse(
            codigo=result.codigo,
            sigla=result.sigla,
            formula=result.formula,
            nombre=result.nombre,
            descripcion=result.descripcion,
            procedimiento=result.procedimiento,
            cod_proyecto_fk=result.cod_proyecto_fk,
            cod_unidad_fk=result.cod_unidad_fk,
            peso=result.peso,
            cod_padre_fk=result.cod_padre_fk,
            proyecto_detalle=proyecto_detalle,
            unidad_detalle=unidad_detalle
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(indicador_response))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@indicador_router.get('/indicador', tags= ['indicador'], response_model=List[Indicador])
def get_indicador_by_name(
    name:str = Query(None),
    cod_proyecto_fk: int = Query(None)
    ) -> List[Indicador]:
    try:
        db = SessionLocal()
        result = IndicadorService(db).get_by_indicador(name, cod_proyecto_fk)
        result_dict_list = []
        for proyecto in result:
            proyecto_detalle = {
                "codigo": proyecto.proyecto_distrito_termicos.codigo,
                "nombre": proyecto.proyecto_distrito_termicos.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos.descripcion
            }
            unidad_detalle = {
                "codigo": proyecto.unidades_dt.codigo,
                "unidad": proyecto.unidades_dt.unidad,
                "descripcion": proyecto.unidades_dt.descripcion 
            }   
            indicador_response = IndicadorResponse(
                codigo=proyecto.codigo,
                sigla=proyecto.sigla,
                formula=proyecto.formula,
                nombre=proyecto.nombre,
                descripcion=proyecto.descripcion,
                procedimiento=proyecto.procedimiento,
                cod_proyecto_fk=proyecto.cod_proyecto_fk,
                cod_unidad_fk=proyecto.cod_unidad_fk,
                peso=proyecto.peso,
                cod_padre_fk=proyecto.cod_padre_fk,
                proyecto_detalle=proyecto_detalle,
                unidad_detalle=unidad_detalle
                )
            result_dict_list.append(indicador_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@indicador_router.post('/indicador', tags=['indicador'], response_model= dict, status_code=201)
def post_indicador(indicador: Indicador) -> dict:
    try:
        db = SessionLocal()
        IndicadorService(db).create_indicador(indicador)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el indicador"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@indicador_router.patch('/indicador/{codigo}', tags=['indicador'], response_model= Indicador, status_code=201)
async def patch_indicador(codigo: int, item_update:IndicadorUpdate):
    try:
        db = SessionLocal()
        result = IndicadorService(db).get_indicador_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        indicador_data = item_update.dict(exclude_unset=True)
        IndicadorService(db).patch_indicador(codigo, indicador_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el indicador"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@indicador_router.delete('/indicador/{codigo}', tags=['indicador'], response_model=dict, status_code=200)
async def delete_indicador(codigo:int) -> dict:
    db = SessionLocal()
    result = IndicadorService(db).get_indicador_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    IndicadorService(db).delete_indicador(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el indicador"})
