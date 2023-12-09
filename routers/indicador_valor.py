from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.indicador_valor import IndicadorValorService
from schemas.indicador_valor import IndicadorDetalle, IndicadorValor, IndicadorValorResponse, ProyectoDetalle, EscenarioDetalle
from models.indicador_valor import IndicadorValorModel
from geoalchemy2.shape import to_shape, from_shape


indicador_valor_router = APIRouter()

@indicador_valor_router.get('/indicador_valor',tags=['indicador_valor'], response_model=List[IndicadorValor], status_code=200)
async def get_indicador() -> List[IndicadorValor]:
    try:
        db = SessionLocal()
        result = IndicadorValorService(db).get_indicadorValor()
        result_dict_list = []
        for proyecto in result:
            ProyectoDetalle = {
                "codigo": proyecto.proyecto_distrito_termicos_sal.codigo,
                "nombre": proyecto.proyecto_distrito_termicos_sal.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos_sal.descripcion
            }
            UerDetalle = {
                "codigo": proyecto.unidad_espacial_sal.codigo,
                "geom": to_shape(proyecto.unidad_espacial_sal.geom).__geo_interface__,
            }
            IndicadorDetalle = {
                "codigo": proyecto.indicador_sal.codigo,
                "nombre": proyecto.indicador_sal.nombre,
                "descripcion": proyecto.indicador_sal.descripcion
            }
            EscenarioDetalle = {
                "codigo": proyecto.escenario_sal.codigo,
                "nombre": proyecto.escenario_sal.nombre,
                "estado": proyecto.escenario_sal.estado,
                "sincronizado": proyecto.escenario_sal.sincronizado
            }   
            indicador_response = IndicadorValorResponse(
                codigo= proyecto.codigo,
                valor= proyecto.valor,
                cod_uer_fk= proyecto.cod_uer_fk,
                cod_indicador_fk= proyecto.cod_indicador_fk,
                cod_proyecto_fk= proyecto.cod_proyecto_fk,
                valor_ponderado= proyecto.valor_ponderado,
                cod_ind_padre_fk= proyecto.cod_ind_padre_fk,
                cod_escenario_fk= proyecto.cod_escenario_fk,
                uer_detalle=UerDetalle,
                indicador_detalle=IndicadorDetalle,
                proyecto_detalle=ProyectoDetalle,
                escenario_detalle = EscenarioDetalle,
            )
            result_dict_list.append(indicador_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@indicador_valor_router.get('/indicador_valor/', tags= ['indicador_valor'], response_model=List[IndicadorValor])
def get_indicador_by_name(cod_proyecto:int = None, cod_indicador:int = None, cod_escenario:int = None) -> List[IndicadorValor]:
    try:
        db = SessionLocal()
        result = IndicadorValorService(db).get_by_criteria(cod_proyecto, cod_indicador, cod_escenario)
        result_dict_list = []
        for proyecto in result:
            ProyectoDetalle = {
                "codigo": proyecto.proyecto_distrito_termicos_sal.codigo,
                "nombre": proyecto.proyecto_distrito_termicos_sal.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos_sal.descripcion
            }
            UerDetalle = {
                "codigo": proyecto.unidad_espacial_sal.codigo,
                "geom": to_shape(proyecto.unidad_espacial_sal.geom).__geo_interface__,
            }
            IndicadorDetalle = {
                "codigo": proyecto.indicador_sal.codigo,
                "nombre": proyecto.indicador_sal.nombre,
                "descripcion": proyecto.indicador_sal.descripcion
            }
            EscenarioDetalle = {
                "codigo": proyecto.escenario_sal.codigo,
                "nombre": proyecto.escenario_sal.nombre,
                "estado": proyecto.escenario_sal.estado,
                "sincronizado": proyecto.escenario_sal.sincronizado
            }   
            indicador_response = IndicadorValorResponse(
                codigo= proyecto.codigo,
                valor= proyecto.valor,
                cod_uer_fk= proyecto.cod_uer_fk,
                cod_indicador_fk= proyecto.cod_indicador_fk,
                cod_proyecto_fk= proyecto.cod_proyecto_fk,
                valor_ponderado= proyecto.valor_ponderado,
                cod_ind_padre_fk= proyecto.cod_ind_padre_fk,
                cod_escenario_fk= proyecto.cod_escenario_fk,
                uer_detalle=UerDetalle,
                indicador_detalle=IndicadorDetalle,
                proyecto_detalle=ProyectoDetalle,
                escenario_detalle = EscenarioDetalle,
            )
            result_dict_list.append(indicador_response)
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict_list))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))