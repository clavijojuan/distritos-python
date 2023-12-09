from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.escenario import EscenarioService
from schemas.escenario import Escenario, EscenarioQuery, EscenarioUpdate, EscenarioIndicadorInsumoDetalle, EscenarioResponse
from models.escenario import escenario_model
from models.escenario_indicador_insumo import EscenarioIndicadorInsumoModel
from models.indicador import IndicadorModel
from sqlalchemy.orm import joinedload
from models.simbologia_indicador import SimbologiaIndicadorModel
from routers.fn_indicador_valor_fija import execute_fn_indicador_valor_fija
from routers.fn_indicador_valor_padre_fija import execute_fn_indicador_valor_padre_fija

escenario_router = APIRouter()

'''
@escenario_router.get('/escenario',tags=['escenario'], response_model=List[Escenario], status_code=200)
async def get_escenario() -> List[Escenario]:
    try:
        db = SessionLocal()
        result = EscenarioService(db).get_escenario()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

@escenario_router.get('/escenario/{codigo}', tags= ['escenario'], response_model=Escenario)
def get_escenario_by_id(codigo: int) -> Escenario:
    try:
        db = SessionLocal()
        result = EscenarioService(db).get_escenario_by_id(codigo)
        if not result:
            return JSONResponse(status_code=200, content=[])
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

'''
@escenario_router.get('/escenario', tags= ['escenario'], response_model=List[Escenario])
def get_escenario_by_name(escenario:str = Query(None)) -> List[Escenario]:
    try:
        db = SessionLocal()
        result = EscenarioService(db).get_by_escenario(escenario)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''    
'''
@escenario_router.get('/escenario', tags=['escenario'], response_model=List[EscenarioResponse])
def get_escenario_by_name(escenario: str = Query(None)) -> List[EscenarioResponse]:
    try:
        db = SessionLocal()
        results = EscenarioService(db).get_by_escenario(escenario)
        
        escenario_responses = []
        for result in results:
            escenario_indicador_insumo_detalle = []
            if result.escenarios:
                escenario_indicador_insumo = result.escenarios[0]
                detalle = {
                    "cod_indicador_fk": escenario_indicador_insumo.cod_indicador_fk,
                }
                escenario_indicador_insumo_detalle.append(detalle)
            
            escenario_response = EscenarioResponse(
                sincronizado=result.sincronizado,
                nombre=result.nombre,
                estado=result.estado,
                escenario_insumo_indicador_detalle=escenario_indicador_insumo_detalle,
            )
            escenario_responses.append(escenario_response)
        
        return escenario_responses
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
'''

@escenario_router.get('/escenario', tags=['escenario'], response_model=List[EscenarioResponse])
def get_escenario_by_name(escenario: str = Query(None), codigo: int = Query(None)) -> List[EscenarioResponse]:
    try:
        db = SessionLocal()
        results = EscenarioService(db).get_by_escenario(escenario, codigo)
        
        escenario_responses = []
        for result in results:
            escenario_indicador_insumo_detalle = []
            if result.escenarios:
                escenario_indicador_insumo = result.escenarios[0]

                indicador_info = (
                    db.query(IndicadorModel)
                    .filter(IndicadorModel.codigo == escenario_indicador_insumo.cod_indicador_fk)
                    .first()
                )

                proyecto_distrito_termicos = [
                    {
                        "codigo": indicador_info.proyecto_distrito_termicos.codigo,
                        "nombre": indicador_info.proyecto_distrito_termicos.nombre,
                        "descripcion": indicador_info.proyecto_distrito_termicos.descripcion,
                    }
                ]

                detalle = {
                    "proyecto_distrito_termicos": proyecto_distrito_termicos,
                }
                escenario_indicador_insumo_detalle.append(detalle)

                sincronizado = result.sincronizado if result.sincronizado is not None else False
            
            escenario_response = EscenarioResponse(
                codigo= result.codigo,
                sincronizado=result.sincronizado,
                nombre=result.nombre,
                estado=result.estado,
                escenario_insumo_indicador_detalle=escenario_indicador_insumo_detalle,
            )
            escenario_responses.append(escenario_response)
        
        return escenario_responses
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@escenario_router.post('/escenario', tags=['escenario'], response_model= dict, status_code=201)
def post_escenario(escenario: Escenario) -> dict:
    try:
        db = SessionLocal()
        EscenarioService(db).create_escenario(escenario)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el escenario"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@escenario_router.patch('/escenario/{codigo}', tags=['escenario'], response_model= Escenario, status_code=201)
async def patch_escenario(codigo: int, item_update:EscenarioUpdate):
    try:
        db = SessionLocal()
        result = EscenarioService(db).get_escenario_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        escenario_data = item_update.dict(exclude_unset=True)
        sincronizado = escenario_data.get("sincronizado",False)

        if sincronizado:
            result_1 = await execute_fn_indicador_valor_fija(codigo)
            result_2 = await execute_fn_indicador_valor_padre_fija(codigo)
        EscenarioService(db).patch_escenario(codigo, escenario_data)
        return JSONResponse(status_code=201,content={"message":"Se ha registrado el escenario"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@escenario_router.delete('/escenario/{codigo}', tags=['escenario'], response_model=dict, status_code=200)
async def delete_escenario(codigo:int) -> dict:
    try:
        db = SessionLocal()
        result = EscenarioService(db).get_escenario_by_id(codigo)
        if not result:
            return JSONResponse(status_code=404, content={'message':"No encontrado"})
        EscenarioService(db).delete_escenario(codigo)
        return JSONResponse(status_code=200, content={"message":"Se ha eliminado el escenario"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@escenario_router.get('/escenario_consulta', tags=['escenario'], response_model=List[EscenarioResponse])
def get_escenario_consulta(escenario: str = Query(None),  codigo: int = Query(None)) -> List[EscenarioResponse]:
    try:
        db = SessionLocal()
        results = EscenarioService(db).get_by_escenario(escenario, codigo)
        
        escenario_responses = []
        for result in results:
            escenario_indicador_insumo_detalle = []
            if result.escenarios:
                escenario_indicador_insumo = result.escenarios[0]

                indicador_info = (
                    db.query(IndicadorModel)
                    .filter(IndicadorModel.codigo == escenario_indicador_insumo.cod_indicador_fk)
                    .first()
                )

                if indicador_info:
                    detalle_indicador=[
                        {
                            "codigo": indicador_info.codigo,
                            "nombre": indicador_info.nombre
                        }
                    ]

                    simbologia_info_list = (
                        db.query(SimbologiaIndicadorModel)
                        .filter(SimbologiaIndicadorModel.cod_indicador_fk == indicador_info.codigo)
                        .all()
                    )

                    simbologia_indicador = []
                    for simbologia_info in simbologia_info_list:
                        simbologia = {
                            "codigo": simbologia_info.codigo,
                            "cod_indicador_fk": simbologia_info.cod_indicador_fk,
                            "categoria": simbologia_info.categoria,
                            "minimo": simbologia_info.minimo,
                            "maximo": simbologia_info.maximo,
                            "color_r": simbologia_info.color_r,
                            "color_g": simbologia_info.color_g,
                            "color_b": simbologia_info.color_b,
                            "descripcion": simbologia_info.descripcion,
                            "rgb_expression": "rgb({}, {}, {})".format(simbologia_info.color_r, simbologia_info.color_g, simbologia_info.color_b),
                            "hex_color": "#{:02x}{:02x}{:02x}".format(simbologia_info.color_r, simbologia_info.color_g, simbologia_info.color_b)
                        }
                        simbologia_indicador.append(simbologia)

                    proyecto_distrito_termicos = [
                        {
                            "codigo": indicador_info.proyecto_distrito_termicos.codigo,
                            "nombre": indicador_info.proyecto_distrito_termicos.nombre,
                            "descripcion": indicador_info.proyecto_distrito_termicos.descripcion,
                        }
                    ]

                    detalle = {
                        "indicador_detalle": detalle_indicador,
                        "proyecto_distrito_termicos": proyecto_distrito_termicos,
                        "simbologia_indicador": simbologia_indicador
                    }
                    escenario_indicador_insumo_detalle.append(detalle)
            
            escenario_response = EscenarioResponse(
                codigo= result.codigo,
                sincronizado=result.sincronizado,
                nombre=result.nombre,
                estado=result.estado,
                escenario_insumo_indicador_detalle=escenario_indicador_insumo_detalle,
            )
            escenario_responses.append(escenario_response)
        
        return escenario_responses
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
