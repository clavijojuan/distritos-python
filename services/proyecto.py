from models.proyecto import ProyectoDistritoTermico
from schemas.proyecto import Proyecto
from sqlalchemy.sql import or_
from shapely.geometry import shape

class ProyectoService():

    def __init__(self, db) -> None:
        self.db = db

    def get_proyecto(self):
        result = self.db.query(ProyectoDistritoTermico).all()
        return result
    
    def get_proyecto_by_id(self, codigo):
        result = self.db.query(ProyectoDistritoTermico).filter(ProyectoDistritoTermico.codigo == codigo).first()
        return result
    
    
    def get_by_proyecto(self, texto):
        if texto is None or texto == "":
            return self.db.query(ProyectoDistritoTermico).all()

        busqueda_filtro = or_(
            ProyectoDistritoTermico.descripcion.ilike(f"%{texto}%"),
            ProyectoDistritoTermico.nombre.ilike(f"%{texto}%")
        )
        result = self.db.query(ProyectoDistritoTermico).filter(busqueda_filtro).all()
        return result
    
    def create_proyecto(self, proyecto: Proyecto):
        new_proyecto = ProyectoDistritoTermico(**proyecto)
        self.db.add(new_proyecto)
        self.db.commit()
        return

    def patch_proyecto(self, codigo:int, item_update: Proyecto):
        db_item = self.db.query(ProyectoDistritoTermico).filter(ProyectoDistritoTermico.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_proyecto(self, codigo:int):
        self.db.query(ProyectoDistritoTermico).filter(ProyectoDistritoTermico.codigo == codigo).delete()
        self.db.commit()
        return 
