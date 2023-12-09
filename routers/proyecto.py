from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.proyecto import ProyectoService
from schemas.proyecto import Proyecto, ProyectoUpdate, ProyectoQuery
from models.proyecto import ProyectoDistritoTermico
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import shape


proyecto_router = APIRouter()
'''
@proyecto_router.get('/proyectos',tags=['proyectos'], response_model=List[Proyecto], status_code=200)
async def get_proyectos(include_geom: bool = Query(True, description="Incluir campo geometría en la respuesta")) -> List[Proyecto]:
    try:
        db = SessionLocal()
        proyecto_service = ProyectoService(db)
        result = proyecto_service.get_proyecto()
        result_dict_list = []
        for proyecto in result:
            proyecto_dict = {
                "codigo": proyecto.codigo,
                "nombre": proyecto.nombre,
                "descripcion": proyecto.descripcion
            }
            if include_geom:
                proyecto_dict["geom"] = to_shape(proyecto.geom).__geo_interface__
            result_dict_list.append(proyecto_dict)
        return JSONResponse(status_code=200, content=result_dict_list)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

@proyecto_router.get('/proyectos/{codigo}', tags= ['proyectos'], response_model=Proyecto)
async def get_proyectos_by_id(codigo: int, include_geom: bool = Query(True, description="Incluir campo geometría en la respuesta")) -> Proyecto:
    db = SessionLocal()
    result = ProyectoService(db).get_proyecto_by_id(codigo)
    if not result:
        return JSONResponse(status_code=200, content=[])
    result_dict_list = []
    proyecto_dict = {
        "codigo": result.codigo,
        "nombre": result.nombre,
        "descripcion": result.descripcion
        }
    if include_geom:
            proyecto_dict["geom"] = to_shape(result.geom).__geo_interface__
    result_dict_list.append(proyecto_dict)
    return JSONResponse(status_code=200, content=result_dict_list)

@proyecto_router.get('/proyectos', tags= ['proyectos'], response_model=List[ProyectoQuery])
async def get_proyecto_by_field(query_param: str = Query(None,texto="texto a buscar"), include_geom:bool = Query(True,description="Incluir campo geometría en la respuesta")):
    db = SessionLocal()
    result = ProyectoService(db).get_by_proyecto(query_param)
    if not result:
        return JSONResponse(status_code=200, content=[])
    result_dict_list = []
    for proyecto in result:
        proyecto_dict = {
            "codigo": proyecto.codigo,
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion
        }
        if include_geom:
            proyecto_dict["geom"]= to_shape(proyecto.geom).__geo_interface__
        result_dict_list.append(proyecto_dict)
    return JSONResponse(status_code=200, content=result_dict_list)
    
@proyecto_router.post('/proyectos', tags=['proyectos'], response_model= dict, status_code=201)
#def post_movies(id:int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str= Body()):
async def post_proyecto(proyecto: Proyecto) -> dict:
    try:
        db = SessionLocal()
        result_dict_list = []
        prueba = dict(proyecto)
        geo = shape(prueba['geom'])
        wkt = geo.wkt
        proyecto_dict = {
                "nombre": prueba['nombre'],
                "descripcion": prueba['descripcion'],
                "geom": wkt
                }
        ProyectoService(db).create_proyecto(proyecto_dict)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el proyecto"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@proyecto_router.patch('/proyectos/{codigo}', tags=['proyectos'], response_model= Proyecto, status_code=201)
async def patch_proyecto(codigo: int, item_update: ProyectoUpdate):
    try:
        db = SessionLocal()
        result = ProyectoService(db).get_proyecto_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        proyecto_data = item_update.dict(exclude_unset=True)
        if (proyecto_data['geom']):
            proyecto_data['geom'] = shape(proyecto_data['geom']).wkt
        ProyectoService(db).patch_proyecto(codigo, proyecto_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el proyecto"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@proyecto_router.delete('/proyectos/{codigo}', tags=['proyectos'], response_model=dict, status_code=200)
async def delete_movie(codigo:int) -> dict:
    db = SessionLocal()
    result = ProyectoService(db).get_proyecto_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    ProyectoService(db).delete_proyecto(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el proyecto"})