from models.unidad_espacial_referencia_dt import UnidadEspacialReferenciaModel
from schemas.unidad_espacial_referencia_dt import UnidadEspacialReferencia
from sqlalchemy.sql import or_
from shapely.geometry import shape

class UnidadEspacialReferenciaService():

    def __init__(self, db) -> None:
        self.db = db

    def get_uer(self):
        result = self.db.query(UnidadEspacialReferenciaModel).order_by(UnidadEspacialReferenciaModel.codigo.desc()).limit(100)
        return result
    
    def get_uer_by_id(self, cod_proyecto_fk):
        result = self.db.query(UnidadEspacialReferenciaModel).filter(UnidadEspacialReferenciaModel.cod_proyecto_fk == cod_proyecto_fk).limit(100)
        return result
    
    
    def get_by_uer(self, texto):
        busqueda_filtro = or_(
            UnidadEspacialReferenciaModel.descripcion.ilike(f"%{texto}%"),
            UnidadEspacialReferenciaModel.nombre.ilike(f"%{texto}%")
        )
        result = self.db.query(UnidadEspacialReferenciaModel).filter(busqueda_filtro).all()
        return result
    
    def create_uer(self, uer: UnidadEspacialReferencia):
        new_uer = UnidadEspacialReferenciaModel(**uer)
        self.db.add(new_uer)
        self.db.commit()
        return

    def patch_uer(self, cod_proyecto_fk:int, field_updates: dict[str,str]):
        db_item = self.db.query(UnidadEspacialReferenciaModel).filter(UnidadEspacialReferenciaModel.cod_proyecto_fk == cod_proyecto_fk).all()
        for dato in db_item:
            for field,value in field_updates.items():
                setattr(dato, field, value)
        self.db.commit()
        return

    def delete_uer(self, cod_proyecto_fk:int):
        self.db.query(UnidadEspacialReferenciaModel).filter(UnidadEspacialReferenciaModel.cod_proyecto_fk == cod_proyecto_fk).delete()
        self.db.commit()
        return 
