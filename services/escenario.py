from models.escenario import escenario_model
from models.escenario_indicador_insumo import EscenarioIndicadorInsumoModel
from models.indicador import IndicadorModel
from schemas.escenario import Escenario, EscenarioQuery, EscenarioUpdate
from sqlalchemy.sql import or_
from sqlalchemy.orm import joinedload
from typing import Optional

class EscenarioService():

    def __init__(self, db) -> None:
        self.db = db

    def get_escenario(self):
        result = self.db.query(escenario_model).all()
        return result
    
    def get_escenario_by_id(self, codigo):
        result = self.db.query(escenario_model).filter(escenario_model.codigo == codigo).first()
        return result
    
    
    def get_by_escenario(self, escenario=None, codigo=None):
        query = self.db.query(escenario_model)

        if escenario is not None and escenario != "":
            busqueda_filtro = escenario_model.nombre.ilike(f"%{escenario}%")
            query = query.filter(busqueda_filtro)

        if codigo is not None:
            query = query.filter(escenario_model.codigo == codigo)

        result = query.all()
        return result
    
    
    def create_escenario(self, escenario: Escenario):
        new_escenario = escenario_model(**escenario.dict())
        self.db.add(new_escenario)
        self.db.commit()
        return

    def patch_escenario(self, codigo:int, item_update: Escenario):
        db_item = self.db.query(escenario_model).filter(escenario_model.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_escenario(self, codigo:int):
        self.db.query(escenario_model).filter(escenario_model.codigo == codigo).delete()
        self.db.commit()
        return 
