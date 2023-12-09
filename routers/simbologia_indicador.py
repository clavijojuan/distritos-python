from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.simbologia_indicador import SimbologiaIndicadorService
from schemas.simbologia_indicador import SimbologiaIndicador, SimbologiaIndicadorResponse, SimbologiaIndicadorUpdate, IndicadorDetalle
from models.simbologia_indicador import SimbologiaIndicadorModel


simbologia_indicador_router = APIRouter()

@simbologia_indicador_router.get('/simbologia_indicador',tags=['simbologia_indicador'], response_model=List[SimbologiaIndicador], status_code=200)
async def get_simbologia_indicador(cod_indicador_fk: int = Query(None),descripcion:str = Query(None)) -> List[SimbologiaIndicador]:
    try:
        db = SessionLocal()
        result = SimbologiaIndicadorService(db).get_simbologia_indicador(cod_indicador_fk, descripcion)
        result_dict_list = []
        for proyecto in result:
            indicador_detalle = {
                "codigo": proyecto.indicador_dt.codigo,
                "nombre": proyecto.indicador_dt.nombre,
                "descripcion": proyecto.indicador_dt.descripcion
            }
            simbologia_indicador_response = SimbologiaIndicadorResponse(
                codigo=proyecto.codigo,
                cod_indicador_fk= proyecto.cod_indicador_fk,
                categoria=proyecto.categoria,
                minimo=proyecto.minimo,
                maximo=proyecto.maximo,
                color_r=proyecto.color_r,
                color_g=proyecto.color_g,
                color_b=proyecto.color_b,
                descripcion=proyecto.descripcion,
                indicador_detalle=indicador_detalle,
                rgb_expression=f"rgb({proyecto.color_r}, {proyecto.color_g}, {proyecto.color_b})",
                hex_color="#{:02X}{:02X}{:02X}".format(proyecto.color_r, proyecto.color_g, proyecto.color_b)
                )
            result_dict_list.append(simbologia_indicador_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@simbologia_indicador_router.get('/simbologia_indicador/{codigo}', tags= ['simbologia_indicador'], response_model=SimbologiaIndicador)
def get_simbologia_indicador_by_id(codigo: int) -> SimbologiaIndicador:
    try:
        db = SessionLocal()
        result = SimbologiaIndicadorService(db).get_simbologia_indicador_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        
        proyecto_detalle = {
            "codigo": result.indicador_dt.codigo,
            "nombre": result.indicador_dt.nombre,
            "descripcion": result.indicador_dt.descripcion
        }
        simbologia_indicador_response = SimbologiaIndicadorResponse(
            codigo=result.codigo,
            cod_indicador_fk= result.cod_indicador_fk,
            categoria=result.categoria,
            minimo=result.minimo,
            maximo=result.maximo,
            color_r=result.color_r,
            color_g=result.color_g,
            color_b=result.color_b,
            descripcion=result.descripcion,
            indicador_detalle=proyecto_detalle,
            rgb_expression=f"rgb({result.color_r}, {result.color_g}, {result.color_b})",
            hex_color="#{:02X}{:02X}{:02X}".format(result.color_r, result.color_g, result.color_b)
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(simbologia_indicador_response))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''
@simbologia_indicador_router.get('/simbologia_indicador/', tags= ['simbologia_indicador'], response_model=List[SimbologiaIndicador])
def get_simbologia_indicador_by_name(name:str = Query()) -> List[SimbologiaIndicador]:
    try:
        db = SessionLocal()
        result = SimbologiaIndicadorService(db).get_by_simbologia_indicador(name)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''   
    
@simbologia_indicador_router.post('/simbologia_indicador', tags=['simbologia_indicador'], response_model= dict, status_code=201)
def post_simbologia_indicador(simbologia_indicador: SimbologiaIndicador) -> dict:
    try:
        db = SessionLocal()
        SimbologiaIndicadorService(db).create_simbologia_indicador(simbologia_indicador)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la simbología"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@simbologia_indicador_router.patch('/simbologia_indicador/{codigo}', tags=['simbologia_indicador'], response_model= SimbologiaIndicador, status_code=201)
async def patch_simbologia_indicador(codigo: int, item_update:SimbologiaIndicadorUpdate):
    try:
        db = SessionLocal()
        result = SimbologiaIndicadorService(db).get_simbologia_indicador_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        proyecto_data = item_update.dict(exclude_unset=True)
        SimbologiaIndicadorService(db).patch_simbologia_indicador(codigo, proyecto_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la simbología"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@simbologia_indicador_router.delete('/simbologia_indicador/{codigo}', tags=['simbologia_indicador'], response_model=dict, status_code=200)
async def delete_simbologia_indicador(codigo:int) -> dict:
    db = SessionLocal()
    result = SimbologiaIndicadorService(db).get_simbologia_indicador_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    SimbologiaIndicadorService(db).delete_simbologia_indicador(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el registro"})
