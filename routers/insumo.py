from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.insumo import InsumoService
from schemas.insumo import Insumo, InsumoUpdate, InsumoResponse
from models.insumo import InsumoModel
from services.insumo_temporal_geom import InsumoTemporalGeomService
from schemas.insumo_temporal_geom import InsumoTemporalGeom
from routers.insumo_temporal_geom import post_insumo_temporal
from services.fn_rasterizar_recorte_insumo import FnRasterizarRecorteInsumoService
from routers.fn_rasterizar_recorte_insumo import execute_fn_rasterizar_recorte


insumo_router = APIRouter()
insumo_temporal_geom_router = APIRouter()

@insumo_router.get('/insumo',tags=['insumo'], response_model=List[Insumo], status_code=200)
async def get_insumo(name:str = Query(None), cod_proyecto_fk: int = Query(None)) -> List[Insumo]:
    try:
        db = SessionLocal()
        '''
        if name:
        '''
        result = InsumoService(db).get_by_insumo(name, cod_proyecto_fk)
        '''
        else:
            result = InsumoService(db).get_insumo()
        '''    
        result_dict_list = []
        for proyecto in result:
            proyecto_detalle = {
                "codigo": proyecto.proyecto_distrito_termicos.codigo,
                "nombre": proyecto.proyecto_distrito_termicos.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos.descripcion
            }
            insumo_response = InsumoResponse(
                codigo=proyecto.codigo,
                nombre=proyecto.nombre,
                descripcion=proyecto.descripcion,
                cod_proyecto_fk=proyecto.cod_proyecto_fk,
                campo_calculado=proyecto.campo_calculado,
                sigla=proyecto.sigla,
                proyecto_detalle=proyecto_detalle
                )
            result_dict_list.append(insumo_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@insumo_router.get('/insumo/{codigo}', tags= ['insumo'], response_model=Insumo)
def get_insumo_by_id(codigo: int) -> Insumo:
    try:
        db = SessionLocal()
        result = InsumoService(db).get_insumo_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        
        proyecto_detalle = {
            "codigo": result.proyecto_distrito_termicos.codigo,
            "nombre": result.proyecto_distrito_termicos.nombre,
            "descripcion": result.proyecto_distrito_termicos.descripcion
        }
        insumo_response = InsumoResponse(
            codigo=result.codigo,
            nombre=result.nombre,
            descripcion=result.descripcion,
            cod_proyecto_fk=result.cod_proyecto_fk,
            campo_calculado=result.campo_calculado,
            sigla=result.sigla,
            proyecto_detalle=proyecto_detalle
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(insumo_response))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

'''
@insumo_router.get('/insumo/', tags= ['insumo'], response_model=List[Insumo])
def get_insumo_by_name(name:str = Query()) -> List[Insumo]:
    try:
        db = SessionLocal()
        result = InsumoService(db).get_by_insumo(name)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''    
    
@insumo_router.post('/insumo', tags=['insumo'], response_model= dict, status_code=201)
async def post_insumo(insumo: Insumo) -> dict:
    try:
        db = SessionLocal()
        InsumoService(db).create_insumo(insumo)

        last_insumo = db.query(InsumoModel).order_by(InsumoModel.codigo.desc()).first()
        print("Último código de insumo:", last_insumo.codigo)
        print("Campo calculado:", last_insumo.campo_calculado)

        if last_insumo:
            insumo_temp = InsumoTemporalGeom(geom=insumo.geom, cod_insumo_fk=last_insumo.codigo)
            result_temporal = await post_insumo_temporal(insumo_temp, campo_calculado_last_insumo=last_insumo.campo_calculado)
            result_fn_rasterizar = await execute_fn_rasterizar_recorte(
                codigo_proyecto=last_insumo.cod_proyecto_fk,
                codigo_insumo=last_insumo.codigo
            )
            return JSONResponse(status_code=201,content={"message":"Se ha registrado el insumo y el insumo temporal"})            
        else:
            return JSONResponse(status_code=404, content={"message": "No se ha creado ningún insumo"})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@insumo_router.patch('/insumo/{codigo}', tags=['insumo'], response_model= Insumo, status_code=201)
async def patch_insumo(codigo: int, item_update:InsumoUpdate):
    try:
        db = SessionLocal()
        result = InsumoService(db).get_insumo_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        proyecto_data = item_update.dict(exclude_unset=True)
        InsumoService(db).patch_insumo(codigo, proyecto_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el insumo"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@insumo_router.delete('/insumo/{codigo}', tags=['insumo'], response_model=dict, status_code=200)
async def delete_insumo(codigo:int) -> dict:
    db = SessionLocal()
    result = InsumoService(db).get_insumo_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    InsumoService(db).delete_insumo(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el insumo"})
