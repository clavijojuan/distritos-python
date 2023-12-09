from sqlalchemy.sql import text
from fastapi import HTTPException
from config.database import SessionLocal
import geojson


class FnRasterizarRecorteInsumoService:

    def __init__(self, db) -> None:
        self.db = db

    def execute_fn_rasterizar_recorte_insumo(self, codigo_proyecto, codigo_insumo):
        try:
            consulta = text(
                'SELECT * FROM public.fn_rasterizar_recorte_insumo( :codigo_proyecto, :codigo_insumo)'
            )
            
            result = self.db.execute(consulta, {
                'codigo_proyecto': codigo_proyecto,
                'codigo_insumo': codigo_insumo
            })
        
            self.db.commit()
            return {"message": "Función ejecutada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
