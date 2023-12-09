from models.indicador_valor import IndicadorValorModel
from schemas.indicador_valor import IndicadorDetalle, IndicadorValor, IndicadorValorResponse, UerDetalle, ProyectoDetalle, EscenarioDetalle
from sqlalchemy.sql import or_, and_

class IndicadorValorService():

    def __init__(self, db) -> None:
        self.db = db

    def get_indicadorValor(self):
        result = self.db.query(IndicadorValorModel).all()
        return result
    
    def get_by_criteria(self, cod_proyecto=None, cod_indicador=None, cod_escenario=None):
        condiciones = []

        if cod_proyecto:
            condiciones.append(
                or_(
                    IndicadorValorModel.cod_proyecto_fk == cod_proyecto
                )
            )
        if cod_indicador:
            condiciones.append(
                or_(
                    IndicadorValorModel.cod_indicador_fk == cod_indicador
                )
            )
        if cod_escenario:
            condiciones.append(
                or_(
                    IndicadorValorModel.cod_escenario_fk == cod_escenario
                )
            )
        if condiciones:
            busqueda_filtro = and_(*condiciones)
            result = self.db.query(IndicadorValorModel).filter(busqueda_filtro).all()
        else:
            result = []
        return result
    
