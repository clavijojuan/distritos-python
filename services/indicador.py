from models.indicador import IndicadorModel
from schemas.indicador import Indicador, IndicadorResponse, IndicadorUpdate
from sqlalchemy.sql import or_
from typing import Optional

class IndicadorService():

    def __init__(self, db) -> None:
        self.db = db

    def get_indicador(self):
        result = self.db.query(IndicadorModel).all()
        return result
    
    def get_indicador_by_id(self, codigo):
        result = self.db.query(IndicadorModel).filter(IndicadorModel.codigo == codigo).first()
        return result
    
    
    def get_by_indicador(self, nombre:str, cod_proyecto_fk: Optional[int]=None):
        query = self.db.query(IndicadorModel)

        if nombre is not None and nombre != "":
            busqueda_filtro = IndicadorModel.nombre.ilike(f"%{nombre}%")
            query = query.filter(busqueda_filtro)

        if cod_proyecto_fk is not None:
            query = query.filter(IndicadorModel.cod_proyecto_fk == cod_proyecto_fk)

        result = query.all()
        return result
    
    def create_indicador(self, indicador: Indicador):
        new_indicador = IndicadorModel(**indicador.dict())
        self.db.add(new_indicador)
        self.db.commit()
        return

    def patch_indicador(self, codigo:int, item_update: Indicador):
        db_item = self.db.query(IndicadorModel).filter(IndicadorModel.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_indicador(self, codigo:int):
        self.db.query(IndicadorModel).filter(IndicadorModel.codigo == codigo).delete()
        self.db.commit()
        return 