from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.indicador_valor_temporal import IndicadorValorTemporalService
from schemas.indicador_valor_temporal import IndicadorDetalle, IndicadorValorTemporalResponse, IndicadorValorTemporal, ProyectoDetalle, EscenarioDetalle
from models.indicador_valor_temporal import IndicadorValorTemporalModel
from geoalchemy2.shape import to_shape, from_shape


indicador_valor_temporal_router = APIRouter()

@indicador_valor_temporal_router.get('/indicador_valor_temporal',tags=['indicador_valor_temporal'], response_model=List[IndicadorValorTemporal], status_code=200)
async def get_indicador() -> List[IndicadorValorTemporal]:
    try:
        db = SessionLocal()
        result = IndicadorValorTemporalService(db).get_indicadorValorTemporal()
        result_dict_list = []
        for proyecto in result:
            ProyectoDetalle = {
                "codigo": proyecto.proyecto_distrito_termicos_sal_temporal.codigo,
                "nombre": proyecto.proyecto_distrito_termicos_sal_temporal.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos_sal_temporal.descripcion
            }
            UerDetalle = {
                "codigo": proyecto.unidad_espacial_sal_temporal.codigo,
                "geom": to_shape(proyecto.unidad_espacial_sal_temporal.geom).__geo_interface__,
            }
            IndicadorDetalle = {
                "codigo": proyecto.indicador_sal_temporal.codigo,
                "nombre": proyecto.indicador_sal_temporal.nombre,
                "descripcion": proyecto.indicador_sal_temporal.descripcion
            }
            EscenarioDetalle = {
                "codigo": proyecto.escenario_sal_temporal.codigo,
                "nombre": proyecto.escenario_sal_temporal.nombre,
                "estado": proyecto.escenario_sal_temporal.estado,
                "sincronizado": proyecto.escenario_sal_temporal.sincronizado
            }   
            indicador_response = IndicadorValorTemporalResponse(
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

@indicador_valor_temporal_router.get('/indicador_valor_temporal/', tags= ['indicador_valor_temporal'], response_model=List[IndicadorValorTemporal])
def get_indicador_by_name(cod_proyecto:int = None, cod_indicador:int = None, cod_escenario:int = None) -> List[IndicadorValorTemporal]:
    try:
        db = SessionLocal()
        result = IndicadorValorTemporalService(db).get_by_criteria(cod_proyecto, cod_indicador, cod_escenario)
        result_dict_list = []
        for proyecto in result:
            ProyectoDetalle = {
                "codigo": proyecto.proyecto_distrito_termicos_sal_temporal.codigo,
                "nombre": proyecto.proyecto_distrito_termicos_sal_temporal.nombre,
                "descripcion": proyecto.proyecto_distrito_termicos_sal_temporal.descripcion
            }
            UerDetalle = {
                "codigo": proyecto.unidad_espacial_sal_temporal.codigo,
                "geom": to_shape(proyecto.unidad_espacial_sal_temporal.geom).__geo_interface__,
            }
            IndicadorDetalle = {
                "codigo": proyecto.indicador_sal_temporal.codigo,
                "nombre": proyecto.indicador_sal_temporal.nombre,
                "descripcion": proyecto.indicador_sal_temporal.descripcion
            }
            EscenarioDetalle = {
                "codigo": proyecto.escenario_sal_temporal.codigo,
                "nombre": proyecto.escenario_sal_temporal.nombre,
                "estado": proyecto.escenario_sal_temporal.estado,
                "sincronizado": proyecto.escenario_sal_temporal.sincronizado
            }   
            indicador_response = IndicadorValorTemporalResponse(
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