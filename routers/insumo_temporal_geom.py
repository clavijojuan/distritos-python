from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.insumo_temporal_geom import InsumoTemporalGeomService
from schemas.insumo_temporal_geom import InsumoTemporalGeom,InsumoDetalle,InsumoTemporalGeomQuery, InsumoTemporalGeomResponse, InsumoTemporalGeomUpdate
from models.insumo_temporal_geom import InsumoTemporalGeomModel
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import shape
from sqlalchemy.orm import sessionmaker


insumo_tempotal_geom_router = APIRouter()

'''
@insumo_tempotal_geom_router.get('/insumo_temporal',tags=['insumo_temporal'], response_model=List[InsumoTemporalGeom], status_code=200)
async def get_insumo_temporal(include_geom: bool = Query(True, description="Incluir campo geometría en la respuesta")) -> List[InsumoTemporalGeom]:
    try:
        db = SessionLocal()
        insumo_temporal_service = InsumoTemporalGeomService(db)
        result = insumo_temporal_service.get_insumo_temporal()
        result_dict_list = []
        for insumo_temp in result:
            insumo_temp_dict = {
                "codigo": insumo_temp.codigo,
                "campo_calculado": insumo_temp.campo_calculado,
                "cod_insumo_fk": insumo_temp.cod_insumo_fk
            }
            if include_geom:
                insumo_temp_dict["geom"] = to_shape(insumo_temp.geom).__geo_interface__
            result_dict_list.append(insumo_temp_dict)
        return JSONResponse(status_code=200, content=result_dict_list)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''
@insumo_tempotal_geom_router.get('/insumo_temporal/{codigo}', tags= ['insumo_temporal'], response_model=List[InsumoTemporalGeom])
async def get_insumo_temporal_by_id(codigo: int) -> List[InsumoTemporalGeom]:
    try:
        db = SessionLocal()
        insumo_temp_service = InsumoTemporalGeomService(db)
        result = insumo_temp_service.get_insumo_temporal_by_id(codigo)
        result_dict_list = []
        for insumo_temp in result:
            insumo_detalle = {
            "codigo": insumo_temp.insumos_geom_temporal.codigo,
            "nombre": insumo_temp.insumos_geom_temporal.nombre,
            "descripcion": insumo_temp.insumos_geom_temporal.descripcion
            }
            insumo_temp_response = InsumoTemporalGeomResponse(
                codigo=insumo_temp.codigo,
                campo_calculado=insumo_temp.campo_calculado,
                cod_insumo_fk=insumo_temp.cod_insumo_fk,
                geom= to_shape(insumo_temp.geom).__geo_interface__,
                insumos_detalle=insumo_detalle
            )
            result_dict_list.append(insumo_temp_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@insumo_tempotal_geom_router.get('/insumo_temporal', tags= ['insumo_temporal'], response_model=List[InsumoTemporalGeomQuery])
async def get_insumo_temporal_by_field(include_geom: bool = Query(True, description="Incluir campo geometría en la respuesta"),cod_insumo_fk: str = Query(None,texto="texto a buscar")):
    db = SessionLocal()
    result = InsumoTemporalGeomService(db).get_by_insumo_temporal(cod_insumo_fk)
    if not result:
        return JSONResponse(status_code=200, content=[])
    result_dict_list = []
    for insumo_temp in result:
        insumo_detalle = {
            "codigo": insumo_temp.insumos_geom_temporal.codigo,
            "nombre": insumo_temp.insumos_geom_temporal.nombre,
            "descripcion": insumo_temp.insumos_geom_temporal.descripcion
            }
        insumo_temp_response = InsumoTemporalGeomResponse(
                codigo=insumo_temp.codigo,
                campo_calculado=insumo_temp.campo_calculado,
                cod_insumo_fk=insumo_temp.cod_insumo_fk,
                insumos_detalle=insumo_detalle
            )
        if include_geom:
                insumo_temp_response.geom = to_shape(insumo_temp.geom).__geo_interface__
        result_dict_list.append(insumo_temp_response)
    return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    
@insumo_tempotal_geom_router.post('/insumo_temporal', tags=['insumo_temporal'], response_model= dict, status_code=201)
async def post_insumo_temporal(insumo_temporal: InsumoTemporalGeom,campo_calculado_last_insumo: int) -> dict:
    try:
        db = SessionLocal()
        result_dict_list = []

        cod_insumo_fk = insumo_temporal.cod_insumo_fk
        
        for feature in insumo_temporal.geom["features"]:
            geometry = feature["geometry"]
            propiedad = feature["properties"]
            '''campo1_value = propiedad.get("campo1",None)'''
            campo1_value = propiedad.get(str(campo_calculado_last_insumo), None)
            if campo1_value is not None:
                geo = shape(geometry)
                wkt = geo.wkt
                insumo_temp_dict = {
                    "campo_calculado": campo1_value,
                    "geom": wkt,
                    "cod_insumo_fk": cod_insumo_fk,
                }
            InsumoTemporalGeomService(db).create_insumo_temporal(insumo_temp_dict)
        return JSONResponse(status_code=201,content={"message":"Se ha finalizado el registro"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@insumo_tempotal_geom_router.patch('/insumo_temporal/{codigo}', tags=['insumo_temporal'], response_model= InsumoTemporalGeom, status_code=201)
async def patch_insumo_temp(codigo: int, field_updates: dict[str, str]):
    try:
        db = SessionLocal()
        result = InsumoTemporalGeomService(db).get_insumo_temporal_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        InsumoTemporalGeomService(db).patch_insumo_temporal(codigo, field_updates)
        return JSONResponse(status_code=201,content={"message":"Se ha actualizado"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@insumo_tempotal_geom_router.delete('/insumo_temporal/{codigo}', tags=['insumo_temporal'], response_model=dict, status_code=200)
async def delete_insumo_temp(codigo:int) -> dict:
    db = SessionLocal()
    result = InsumoTemporalGeomService(db).get_insumo_temporal_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    InsumoTemporalGeomService(db).delete_insumo_temporal(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el registro"})