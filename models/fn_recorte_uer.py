from sqlalchemy import Column, Integer, String, text
from geoalchemy2 import Geometry
from config.database import Base

class FnRecorteUerModel(Base):
    __tablename__ = "public_fn_recorte_uer"
    

    id = Column(Integer, primary_key=True, autoincrement=True)

    codigo_elemento = Column(Integer, primary_key=False)
    nombre = Column(String, primary_key=False)
    descripcion = Column(String, primary_key=False)
    cod_proyecto_fk = Column(Integer, primary_key=False)
    geojson = Column(String)

    