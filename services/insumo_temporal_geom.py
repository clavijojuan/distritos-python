from models.insumo_temporal_geom import InsumoTemporalGeomModel
from schemas.insumo_temporal_geom import InsumoTemporalGeom
from sqlalchemy.sql import or_
from shapely.geometry import shape

class InsumoTemporalGeomService():

    def __init__(self, db) -> None:
        self.db = db

    def get_insumo_temporal(self):
        result = self.db.query(InsumoTemporalGeomModel).all()
        return result
    
    def get_insumo_temporal_by_id(self, codigo):
        result = self.db.query(InsumoTemporalGeomModel).filter(InsumoTemporalGeomModel.codigo == codigo).all()
        return result
    
    
    def get_by_insumo_temporal(self, cod_insumo_fk):
        if cod_insumo_fk is None or cod_insumo_fk == "":
            return self.db.query(InsumoTemporalGeomModel).all()
        
        busqueda_filtro = InsumoTemporalGeomModel.cod_insumo_fk == cod_insumo_fk
        result = self.db.query(InsumoTemporalGeomModel).filter(busqueda_filtro).all()
        return result
    
    def create_insumo_temporal(self, insumo_temporal: InsumoTemporalGeom):
        new_insumo_temporal = InsumoTemporalGeomModel(**insumo_temporal)
        self.db.add(new_insumo_temporal)
        self.db.commit()
        return

    def patch_insumo_temporal(self, codigo:int, field_updates: dict[str,str]):
        db_item = self.db.query(InsumoTemporalGeomModel).filter(InsumoTemporalGeomModel.codigo == codigo).all()
        for dato in db_item:
            for field,value in field_updates.items():
                setattr(dato, field, value)
        self.db.commit()
        return

    def delete_insumo_temporal(self, codigo:int):
        self.db.query(InsumoTemporalGeomModel).filter(InsumoTemporalGeomModel.codigo == codigo).delete()
        self.db.commit()
        return 
