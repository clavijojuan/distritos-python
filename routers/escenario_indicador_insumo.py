from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.escenario_indicador_insumo import EscenarioIndicadorInsumoService
from schemas.escenario_indicador_insumo import EscenarioDetalle, EscenarioIndicadorInsumo, EscenarioIndicadorInsumoResponse, EscenarioIndicadorInsumoUpdate, IndicadorDetalle, InsumoDetalle
from models.escenario_indicador_insumo import EscenarioIndicadorInsumoModel



escenario_indicador_insumo_router = APIRouter()

@escenario_indicador_insumo_router.get('/escenario_indicador_insumo',tags=['escenario_indicador_insumo'], response_model=List[EscenarioIndicadorInsumo], status_code=200)
async def get_escenario_indicador_insumo(cod_insumo_fk:int = None, cod_indicador_fk:int = None, cod_escenario_fk:int = None) -> List[EscenarioIndicadorInsumo]:
    try:
        db = SessionLocal()
        '''
        result = EscenarioIndicadorInsumoService(db).get_escenario_indicador_insumo()
        '''
        result = EscenarioIndicadorInsumoService(db).get_by_escenario_indicador_insumo(cod_insumo_fk, cod_indicador_fk, cod_escenario_fk)
        result_dict_list = []
        for proyecto in result:
            insumo_detalle = {
                "codigo": proyecto.insumo_dt.codigo,
                "nombre": proyecto.insumo_dt.nombre,
                "descripcion": proyecto.insumo_dt.descripcion
            }
            indicador_detalle = {
                "codigo": proyecto.indicador_dt.codigo,
                "nombre": proyecto.indicador_dt.nombre
            }
            escenario_detalle = {
                "codigo": proyecto.escenario_dt.codigo,
                "nombre": proyecto.escenario_dt.nombre,
                "estado": proyecto.escenario_dt.estado,
                "sincronizado": proyecto.escenario_dt.sincronizado
            }
            insumo_response = EscenarioIndicadorInsumoResponse(
                codigo=proyecto.codigo,
                cod_insumo_fk= proyecto.cod_insumo_fk,
                cod_indicador_fk = proyecto.cod_indicador_fk,
                peso = proyecto.peso,
                cod_escenario_fk = proyecto.cod_escenario_fk,
                insumo_detalle= insumo_detalle,
                indicador_detalle= indicador_detalle,
                escenario_detalle= escenario_detalle,
                )
            result_dict_list.append(insumo_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@escenario_indicador_insumo_router.get('/escenario_indicador_insumo/{codigo}', tags= ['escenario_indicador_insumo'], response_model=EscenarioIndicadorInsumo)
def get_escenario_indicador_insumo_by_id(codigo: int) -> EscenarioIndicadorInsumo:
    try:
        db = SessionLocal()
        result = EscenarioIndicadorInsumoService(db).get_escenario_indicador_insumo_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        insumo_detalle = {
                "codigo": result.insumo_dt.codigo,
                "nombre": result.insumo_dt.nombre,
                "descripcion": result.insumo_dt.descripcion
            }
        indicador_detalle = {
                "codigo": result.indicador_dt.codigo,
                "nombre": result.indicador_dt.nombre
            }
        escenario_detalle = {
                "codigo": result.escenario_dt.codigo,
                "nombre": result.escenario_dt.nombre,
                "estado": result.escenario_dt.estado,
                "sincronizado": result.escenario_dt.sincronizado
            }
        escenario_indicador_insumo_response = EscenarioIndicadorInsumoResponse(
                codigo=result.codigo,
                cod_insumo_fk= result.cod_insumo_fk,
                cod_indicador_fk = result.cod_indicador_fk,
                peso = result.peso,
                cod_escenario_fk = result.cod_escenario_fk,
                insumo_detalle= insumo_detalle,
                indicador_detalle= indicador_detalle,
                escenario_detalle= escenario_detalle,
            )
        return JSONResponse(status_code=200, content=jsonable_encoder(escenario_indicador_insumo_response))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
'''
@escenario_indicador_insumo_router.get('/escenario_indicador_insumo/', tags= ['escenario_indicador_insumo'], response_model=List[EscenarioIndicadorInsumo])
def get_insumo_by_name(name:str = Query()) -> List[EscenarioIndicadorInsumo]:
    try:
        db = SessionLocal()
        result = InsumoService(db).get_by_insumo(name)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''    
'''
@escenario_indicador_insumo_router.post('/escenario_indicador_insumo', tags=['escenario_indicador_insumo'], response_model= dict, status_code=201)
def post_escenario_indicador_insumo(escenario_indicador_insumo: EscenarioIndicadorInsumo) -> dict:
    try:
        db = SessionLocal()
        EscenarioIndicadorInsumoService(db).create_escenario_indicador_insumo(escenario_indicador_insumo)
        return JSONResponse(status_code=201,content={"message":"Se ha generado el registro"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''
@escenario_indicador_insumo_router.post('/escenario_indicador_insumo', tags=['escenario_indicador_insumo'], response_model=dict, status_code=201)
def post_escenario_indicador_insumo(escenario_indicador_insumo: EscenarioIndicadorInsumo) -> dict:
    try:
        db = SessionLocal()
        if sum(escenario_indicador_insumo.peso) != 1.0:
            raise HTTPException(status_code=400, detail="La suma de los pesos debe ser igual a 1")

        items = [
            EscenarioIndicadorInsumoModel(
                cod_insumo_fk=cod_insumo,
                cod_indicador_fk=escenario_indicador_insumo.cod_indicador_fk,
                peso=peso,
                cod_escenario_fk=escenario_indicador_insumo.cod_escenario_fk
            )
            for cod_insumo, peso in zip(escenario_indicador_insumo.cod_insumo_fk, escenario_indicador_insumo.peso)
        ]

        db.add_all(items)
        db.commit()

        return JSONResponse(status_code=201, content={"message": "Se ha generado el registro"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@escenario_indicador_insumo_router.patch('/escenario_indicador_insumo/{codigo}', tags=['escenario_indicador_insumo'], response_model= EscenarioIndicadorInsumo, status_code=201)
async def patch_escenario_indicador_insumo(codigo: int, item_update:EscenarioIndicadorInsumoUpdate):
    try:
        db = SessionLocal()
        result = EscenarioIndicadorInsumoService(db).get_escenario_indicador_insumo_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content={'message':"No encontrado"})
        proyecto_data = item_update.dict(exclude_unset=True)
        EscenarioIndicadorInsumoService(db).patch_escenario_indicador_insumo(codigo, proyecto_data)
        return JSONResponse(status_code=201,content={"message":"Se ha actualizado el registro"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@escenario_indicador_insumo_router.delete('/escenario_indicador_insumo/{codigo}', tags=['escenario_indicador_insumo'], response_model=dict, status_code=200)
async def delete_escenario_indicador_insumo(codigo:int) -> dict:
    db = SessionLocal()
    result = EscenarioIndicadorInsumoService(db).get_escenario_indicador_insumo_by_id(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No encontrado"})
    EscenarioIndicadorInsumoService(db).delete_escenario_indicador_insumo(codigo)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado el registro"})
