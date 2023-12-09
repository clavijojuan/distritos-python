from models.simbologia_indicador import SimbologiaIndicadorModel
from schemas.simbologia_indicador import SimbologiaIndicador, SimbologiaIndicadorUpdate, SimbologiaIndicadorResponse, IndicadorDetalle
from sqlalchemy.sql import or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def find_duplicates(descriptions):
    visited_descriptions = set()
    duplicates = [desc for desc in descriptions if desc in visited_descriptions or visited_descriptions.add(desc)]
    return duplicates

class SimbologiaIndicadorService():

    def __init__(self, db) -> None:
        self.db = db

    def get_simbologia_indicador(self, cod_indicador_fk, descripcion):
        query = self.db.query(SimbologiaIndicadorModel)

        if cod_indicador_fk is not None:
            query = query.filter(SimbologiaIndicadorModel.cod_indicador_fk == cod_indicador_fk)

        if descripcion is not None and descripcion != "":
            query = query.filter(SimbologiaIndicadorModel.descripcion.ilike(f"%{descripcion}%"))

        result = query.all()
        return result
    
    def get_simbologia_indicador_by_id(self, codigo):
        result = self.db.query(SimbologiaIndicadorModel).filter(SimbologiaIndicadorModel.codigo == codigo).first()
        return result
    
    
    def get_by_simbologia_indicador(self, descripcion):
        busqueda_filtro = SimbologiaIndicadorModel.descripcion.ilike(f"%{descripcion}%")
        result = self.db.query(SimbologiaIndicadorModel).filter(busqueda_filtro).all()
        return result
       
    def create_simbologia_indicador(self, simbologia_indicador: SimbologiaIndicador):
        try:
            existing_simbologia = self.db.query(SimbologiaIndicadorModel).filter(
                SimbologiaIndicadorModel.cod_indicador_fk == simbologia_indicador.cod_indicador_fk
            ).first()

            if existing_simbologia:
                raise ValueError(f"Ya existe una simbología para el indicador con código {simbologia_indicador.cod_indicador_fk}")
            

            #validar la longitud de las listas
            if not all(len(lst) == len(simbologia_indicador.categoria) for lst in [
                simbologia_indicador.minimo,
                simbologia_indicador.maximo,
                simbologia_indicador.color_r,
                simbologia_indicador.color_g,
                simbologia_indicador.color_b,
                simbologia_indicador.descripcion
            ]):
                raise ValueError("Las listas de entrada deben tener la misma longitud")
            
            #validar los intervalos
            for i in range(len(simbologia_indicador.categoria)):
                for j in range(i+1, len(simbologia_indicador.categoria)):
                    if (
                        (simbologia_indicador.minimo[i] <= simbologia_indicador.maximo[j] <= simbologia_indicador.maximo[i]) or
                        (simbologia_indicador.minimo[j] <= simbologia_indicador.maximo[i] <= simbologia_indicador.maximo[j])
                    ):
                        print(f"Intervalo {i}: ({simbologia_indicador.minimo[i]}, {simbologia_indicador.maximo[i]})")
                        print(f"Intervalo {j}: ({simbologia_indicador.minimo[j]}, {simbologia_indicador.maximo[j]})")
                        raise ValueError(f"Los intervalos {i} y {j} se superponen")

            for color_r, color_g, color_b in zip(
                simbologia_indicador.color_r,
                simbologia_indicador.color_g,
                simbologia_indicador.color_b,
            ):
                if not (0 <= color_r <= 255) or not (0 <= color_g <= 255) or not (0 <= color_b <= 255):
                    raise ValueError("Los valores de color deben estar en el rango de 0 a 255")       
                
            duplicates = find_duplicates(simbologia_indicador.descripcion)
            if duplicates:
                raise ValueError("Descripciones duplicadas encontradas:", duplicates)


            for cat, min_val, max_val, r, g, b, desc in zip(
                simbologia_indicador.categoria,
                simbologia_indicador.minimo,
                simbologia_indicador.maximo,
                simbologia_indicador.color_r,
                simbologia_indicador.color_g,
                simbologia_indicador.color_b,
                simbologia_indicador.descripcion
            ):
                new_simbologia_indicador = SimbologiaIndicadorModel(
                    cod_indicador_fk = simbologia_indicador.cod_indicador_fk,
                    categoria = cat,
                    minimo = min_val,
                    maximo = max_val,
                    color_r = r,
                    color_g = g,
                    color_b = b,
                    descripcion = desc
                )
                self.db.add(new_simbologia_indicador)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("Error de integridad al agregar simbología: {}".format(e))
        return
    '''
    new_simbologia_indicador = SimbologiaIndicadorModel(**simbologia_indicador.dict())
    self.db.add(new_simbologia_indicador)
    self.db.commit()
    '''    
        

    def patch_simbologia_indicador(self, codigo:int, item_update: SimbologiaIndicador):
        db_item = self.db.query(SimbologiaIndicadorModel).filter(SimbologiaIndicadorModel.codigo == codigo).first()
        for key,value in item_update.items():
            setattr(db_item, key, value)
        self.db.commit()
        return

    def delete_simbologia_indicador(self, codigo:int):
        self.db.query(SimbologiaIndicadorModel).filter(SimbologiaIndicadorModel.codigo == codigo).delete()
        self.db.commit()
        return 