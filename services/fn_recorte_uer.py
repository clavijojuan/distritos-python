from models.fn_recorte_uer import FnRecorteUerModel
from schemas.fn_recorte_uer import FnRecorteUer
from sqlalchemy.sql import text
from fastapi import HTTPException
from config.database import SessionLocal
import geojson


class FnRecorteUerService:

    def __init__(self, db) -> None:
        self.db = db

    def execute_fn_recorte_uer(self, codigo_elemento, nombre, descripcion, cod_proyecto_fk, geojson_dt: str):
        try:
            consulta = text(
                'SELECT * FROM public.fn_recorte_uer( :codigo_elemento, :nombre, :descripcion, :cod_proyecto_fk, :geojson)'
            )
            
            result = self.db.execute(consulta, {
                'codigo_elemento': codigo_elemento,
                'nombre': nombre,
                'descripcion': descripcion,
                'cod_proyecto_fk': cod_proyecto_fk,
                'geojson': geojson_dt
            })
        
            self.db.commit()
            return {"message": "Función ejecutada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    