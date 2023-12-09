from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.error_handler import ErrorHandler


from routers.proyecto import proyecto_router
from routers.unidad import unidad_router
from routers.insumo import insumo_router
from routers.unidad_espacial_referencia_dt import uer_router
from routers.indicador import indicador_router
from routers.escenario import escenario_router
from routers.escenario_indicador_insumo import escenario_indicador_insumo_router
from routers.simbologia_indicador import simbologia_indicador_router
from routers.fn_recorte_uer import routerExec
from routers.fn_rasterizar_recorte_insumo import routerExecRasterizar
from routers.insumo_temporal_geom import insumo_tempotal_geom_router
from routers.fn_indicador_valor_fija import routerExecIndicadorValor
from routers.fn_indicador_valor_padre_fija import routerExecIndicadorValorPadre
from routers.indicador_valor import indicador_valor_router
from routers.indicador_valor_temporal import indicador_valor_temporal_router

app = FastAPI()
app.title = 'Módulo de Distritos Térmicos'
app.description = 'Módulo de Distritos Térmicos de la HaC'
app.version = '1.0'
app.contact = {
    'name': 'ITIM ENGINEERING',
    'email': 'gerencia@itim-engineering.com'
}

origins = [
    "http://localhost:4200",
    'https://6574868f60517d74adc11efe--effulgent-rabanadas-c5e60c.netlify.app',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(ErrorHandler)
app.include_router(proyecto_router)
app.include_router(unidad_router)
app.include_router(insumo_router)
app.include_router(uer_router)
app.include_router(indicador_router)
app.include_router(escenario_router)
app.include_router(escenario_indicador_insumo_router)
app.include_router(simbologia_indicador_router)
app.include_router(routerExec)
app.include_router(insumo_tempotal_geom_router)
app.include_router(routerExecRasterizar)
app.include_router(routerExecIndicadorValor)
app.include_router(routerExecIndicadorValorPadre)
app.include_router(indicador_valor_router)
app.include_router(indicador_valor_temporal_router)


@app.get('/', tags=['index'])
def message():
    return 'Hola mundo'
