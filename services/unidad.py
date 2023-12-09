from models.unidad import unidad_model
from schemas.unidad import Unidad, UnidadQuery, UnidadUpdate
from sqlalchemy.sql import or_

class UnidadService():

    def __init__(self, db) -> None:
        self.db = db

    def get_unidad(self):
        result = self.db.query(unidad_model).all()
        return result
    
    def get_unidad_by_id(self, codigo):
        result = self.db.query(unidad_model).filter(unidad_model.codigo == codigo).first()
        return result
    
    
    def get_by_unidad(self, unidad):
        if unidad is None or unidad == "":
            return self.db.query(unidad_model).all()
        
        busqueda_filtro = unidad_model.unidad.ilike(f"%{unidad}%")
        result = self.db.query(unidad_model).filter(busqueda_filtro).all()
        return result
    
    def create_unidad(self, proyecto: Unidad):
        new_proyecto = unidad_model(**proyecto.dict())
        self.db.add(new_proyecto)
        self.db.commit()
        self.db.refresh(new_proyecto)  # Actualiza el objeto con los valores de la base de datos
        return {"codigo": new_proyecto.codigo}  # Devuelve el código de la unidad creada

    def patch_unidad(self, codigo:int, item_update: Unidad):
        db_item = self.db.query(unidad_model).filter(unidad_model.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_unidad(self, codigo:int):
        self.db.query(unidad_model).filter(unidad_model.codigo == codigo).delete()
        self.db.commit()
        return 
