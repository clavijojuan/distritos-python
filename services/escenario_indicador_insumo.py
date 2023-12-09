from models.escenario_indicador_insumo import EscenarioIndicadorInsumoModel
from schemas.escenario_indicador_insumo import EscenarioIndicadorInsumo, EscenarioIndicadorInsumoUpdate
from sqlalchemy.sql import or_, and_
from typing import List

class EscenarioIndicadorInsumoService():

    def __init__(self, db) -> None:
        self.db = db

    def get_escenario_indicador_insumo(self):
        result = self.db.query(EscenarioIndicadorInsumoModel).all()
        return result
    
    def get_escenario_indicador_insumo_by_id(self, codigo):
        result = self.db.query(EscenarioIndicadorInsumoModel).filter(EscenarioIndicadorInsumoModel.codigo == codigo).first()
        return result
    
    
    def get_by_escenario_indicador_insumo(self, cod_insumo_fk=None, cod_indicador_fk=None, cod_escenario_fk=None):

      condiciones = []

      if cod_insumo_fk:
            condiciones.append(
                or_(
                    EscenarioIndicadorInsumoModel.cod_insumo_fk == cod_insumo_fk
                )
            )
      if cod_indicador_fk:
            condiciones.append(
                or_(
                    EscenarioIndicadorInsumoModel.cod_indicador_fk == cod_indicador_fk
                )
            )
      if cod_escenario_fk:
            condiciones.append(
                or_(
                    EscenarioIndicadorInsumoModel.cod_escenario_fk == cod_escenario_fk
                )
            )
      if condiciones:
            busqueda_filtro = and_(*condiciones)
            result = self.db.query(EscenarioIndicadorInsumoModel).filter(busqueda_filtro).all()
      else:
            result = self.db.query(EscenarioIndicadorInsumoModel).all()
      return result
    
    '''
    def create_escenario_indicador_insumo(self, escenario_indicador_insumo: EscenarioIndicadorInsumo):
        new_escenario_indicador_insumo = EscenarioIndicadorInsumoModel(**escenario_indicador_insumo.dict())
        self.db.add(new_escenario_indicador_insumo)
        self.db.commit()
        return
    '''
    def create_escenario_indicador_insumo(self, escenario_indicador_insumos: List[EscenarioIndicadorInsumo]):
        new_escenario_indicador_insumos = [EscenarioIndicadorInsumoModel(**item.dict()) for item in escenario_indicador_insumos]
        self.db.add_all(new_escenario_indicador_insumos)
        self.db.commit()
        return

    def patch_escenario_indicador_insumo(self, codigo:int, item_update: EscenarioIndicadorInsumo):
        db_item = self.db.query(EscenarioIndicadorInsumoModel).filter(EscenarioIndicadorInsumoModel.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_escenario_indicador_insumo(self, codigo:int):
        self.db.query(EscenarioIndicadorInsumoModel).filter(EscenarioIndicadorInsumoModel.codigo == codigo).delete()
        self.db.commit()
        return 