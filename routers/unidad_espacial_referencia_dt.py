from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.unidad_espacial_referencia_dt import UnidadEspacialReferenciaService
from schemas.unidad_espacial_referencia_dt import UnidadEspacialReferencia, UnidadEspacialReferenciaQuery, UnidadEspacialReferenciaUpdate, UerDetalle, UerResponse
from models.unidad_espacial_referencia_dt import UnidadEspacialReferenciaModel
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import shape


uer_router = APIRouter()


@uer_router.get('/uer',tags=['uer'], response_model=List[UnidadEspacialReferencia], status_code=200)
async def get_uer(include_geom: bool = Query(True, description="Incluir campo geometría en la respuesta")) -> List[UnidadEspacialReferencia]:
    try:
        db = SessionLocal()
        uer_service = UnidadEspacialReferenciaService(db)
        result = uer_service.get_uer()
        result_dict_list = []
        for uer in result:
            uer_dict = {
                "codigo": uer.codigo,
                "nombre": uer.nombre,
                "descripcion": uer.descripcion,
                "cod_proyecto_fk": uer.cod_proyecto_fk,
                "codigo_elemento": uer.codigo_elemento
            }
            if include_geom:
                uer_dict["geom"] = to_shape(uer.geom).__geo_interface__
            result_dict_list.append(uer_dict)
        return JSONResponse(status_code=200, content=result_dict_list)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@uer_router.get('/uer/{cod_proyecto_fk}', tags= ['uer'], response_model=List[UnidadEspacialReferencia])
async def get_uer_by_id(cod_proyecto_fk: int, include_geom:bool = Query(True,description="Incluir campo geometría en la respuesta")) -> List[UnidadEspacialReferencia]:
    try:
        db = SessionLocal()
        uer_service = UnidadEspacialReferenciaService(db)
        result = uer_service.get_uer_by_id(cod_proyecto_fk)

        result_dict_list = []
        for uer in result:
            proyecto_detalle = {
            "codigo": uer.proyecto_distrito_termicos.codigo,
            "nombre": uer.proyecto_distrito_termicos.nombre,
            "descripcion": uer.proyecto_distrito_termicos.descripcion
            }
            uer_response = UerResponse(
                codigo=uer.codigo,
                nombre=uer.nombre,
                descripcion=uer.descripcion,
                cod_proyecto_fk=uer.cod_proyecto_fk,
                codigo_elemento= uer.codigo_elemento,
                proyecto_detalle=proyecto_detalle
            )
            if include_geom:
                uer_response.geom = to_shape(uer.geom).__geo_interface__
            result_dict_list.append(uer_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

'''
@uer_router.get('/uer/', tags= ['uer'], response_model=List[UnidadEspacialReferenciaQuery])
async def get_uer_by_field(query_param: str = Query(...,texto="texto a buscar"), include_geom:bool = Query(True,description="Incluir campo geometría en la respuesta")):
    db = SessionLocal()
    result = UnidadEspacialReferenciaService(db).get_by_uer(query_param)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    result_dict_list = []
    for uer in result:
        proyecto_detalle = {
            "codigo": uer.proyecto_distrito_termicos.codigo,
            "nombre": uer.proyecto_distrito_termicos.nombre,
            "descripcion": uer.proyecto_distrito_termicos.descripcion
            }
        uer_response = UerResponse(
            codigo=uer.codigo,
            nombre=uer.nombre,
            descripcion=uer.descripcion,
            cod_proyecto_fk=uer.cod_proyecto_fk,
            codigo_elemento= uer.codigo_elemento,
            proyecto_detalle=proyecto_detalle
            )
        if include_geom:
            uer_response.geom = to_shape(uer.geom).__geo_interface__
        result_dict_list.append(uer_response)
    return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    '''

    
@uer_router.post('/uer', tags=['uer'], response_model= dict, status_code=201)
async def post_uer(uer: UnidadEspacialReferencia) -> dict:
    try:
        db = SessionLocal()
        result_dict_list = []
        #prueba = dict(uer)
        #print(uer.geom["features"])
        for feature in uer.geom["features"]:
            geometry = feature["geometry"]
            geo = shape(geometry)
            wkt = geo.wkt
            uer_dict = {
                "nombre": uer.nombre,
                "descripcion": uer.descripcion,
                "geom": wkt,
                "cod_proyecto_fk": uer.cod_proyecto_fk,
                "codigo_elemento": uer.codigo_elemento
            }
            UnidadEspacialReferenciaService(db).create_uer(uer_dict)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la Unidad Espacial de Referencia"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@uer_router.patch('/uer/{cod_proyecto_fk}', tags=['uer'], response_model= UnidadEspacialReferencia, status_code=201)
async def patch_uer(cod_proyecto_fk: int, field_updates: dict[str, str]):
    try:
        db = SessionLocal()
        result = UnidadEspacialReferenciaService(db).get_uer_by_id(cod_proyecto_fk)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        UnidadEspacialReferenciaService(db).patch_uer(cod_proyecto_fk, field_updates)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado la Unidad Espacial de Referencia"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@uer_router.delete('/uer/{cod_proyecto_fk}', tags=['uer'], response_model=dict, status_code=200)
async def delete_uer(cod_proyecto_fk:int) -> dict:
    db = SessionLocal()
    result = UnidadEspacialReferenciaService(db).get_uer_by_id(cod_proyecto_fk)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    UnidadEspacialReferenciaService(db).delete_uer(cod_proyecto_fk)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado la Unidad Espacial de Referencia"})