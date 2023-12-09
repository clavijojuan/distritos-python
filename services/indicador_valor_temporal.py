from models.indicador_valor_temporal import IndicadorValorTemporalModel
from schemas.indicador_valor_temporal import IndicadorDetalle, IndicadorValorTemporal, IndicadorValorTemporalResponse, UerDetalle, ProyectoDetalle, EscenarioDetalle
from sqlalchemy.sql import or_, and_
from sqlalchemy.orm import aliased

class IndicadorValorTemporalService():

    def __init__(self, db) -> None:
        self.db = db

    def get_indicadorValorTemporal(self):
        my_view = aliased(IndicadorValorTemporalModel)
        result = self.db.query(my_view).all()
        return result
    
    def get_by_criteria(self, cod_proyecto=None, cod_indicador=None, cod_escenario=None):
        condiciones = []

        if cod_proyecto:
            condiciones.append(
                or_(
                    IndicadorValorTemporalModel.cod_proyecto_fk == cod_proyecto
                )
            )
        if cod_indicador:
            condiciones.append(
                or_(
                    IndicadorValorTemporalModel.cod_indicador_fk == cod_indicador
                )
            )
        if cod_escenario:
            condiciones.append(
                or_(
                    IndicadorValorTemporalModel.cod_escenario_fk == cod_escenario
                )
            )
        if condiciones:
            busqueda_filtro = and_(*condiciones)
            result = self.db.query(IndicadorValorTemporalModel).filter(busqueda_filtro).all()
        else:
            result = []
        return result
    