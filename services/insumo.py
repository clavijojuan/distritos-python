from models.insumo import InsumoModel
from schemas.insumo import Insumo, InsumoUpdate
from sqlalchemy.sql import or_
from geoalchemy2 import WKTElement
from shapely.geometry import shape
from geoalchemy2 import WKTElement
from shapely.geometry import shape
from typing import Optional

class InsumoService():

    def __init__(self, db) -> None:
        self.db = db

    def get_insumo(self):
        result = self.db.query(InsumoModel).all()
        return result
    
    def get_insumo_by_id(self, codigo):
        result = self.db.query(InsumoModel).filter(InsumoModel.codigo == codigo).first()
        return result
    
    
    def get_by_insumo(self, nombre:str, cod_proyecto_fk: Optional[int]=None):
        query = self.db.query(InsumoModel)

        if nombre is not None and nombre != "":
            busqueda_filtro = InsumoModel.nombre.ilike(f"%{nombre}%")
            query = query.filter(busqueda_filtro)
        
        if cod_proyecto_fk is not None:
            query = query.filter(InsumoModel.cod_proyecto_fk == cod_proyecto_fk)

        result = query.all()
        return result
    
            
    def create_insumo(self, insumo: Insumo):
        '''new_insumo = InsumoModel(**insumo.dict())'''
        geom_wkt = shape(insumo.geom["features"][0]["geometry"]).wkt

        new_insumo = InsumoModel(
            nombre=insumo.nombre,
            descripcion=insumo.descripcion,
            cod_proyecto_fk=insumo.cod_proyecto_fk,
            campo_calculado=insumo.campo_calculado,
            sigla=insumo.sigla,
            geom=WKTElement(geom_wkt, srid=9377)  # Asegúrate de especificar el SRID correcto
        )
        self.db.add(new_insumo)
        self.db.commit()
        return

    def patch_insumo(self, codigo:int, item_update: Insumo):
        db_item = self.db.query(InsumoModel).filter(InsumoModel.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_insumo(self, codigo:int):
        self.db.query(InsumoModel).filter(InsumoModel.codigo == codigo).delete()
        self.db.commit()
        return 