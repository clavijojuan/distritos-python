from sqlalchemy.sql import text
from fastapi import HTTPException
from config.database import SessionLocal
import geojson


class FnIndicadorValorPadreFijaService:

    def __init__(self, db) -> None:
        self.db = db

    def execute_fn_indicador_valor_padre_fija(self, codigo_escenario):
        try:
            consulta = text(
                'SELECT * FROM public.fn_indicador_valor_padre_fija( :codigo_escenario)'
            )
            
            result = self.db.execute(consulta, {
                'codigo_escenario': codigo_escenario
            })
        
            self.db.commit()
            return {"message": "Función ejecutada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))