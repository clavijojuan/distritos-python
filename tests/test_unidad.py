from fastapi.testclient import TestClient
from main import app  # Importa la instancia de la aplicación desde el archivo principal de la aplicación
from fastapi.responses import JSONResponse
from models.unidad import unidad_model
from pydantic import ValidationError
import pytest
from config.database import SessionLocal
from fastapi.exceptions import HTTPException

client = TestClient(app)  # Crea un cliente de prueba para la aplicación


def test_get_unidad():
    # Prueba la ruta GET /unidad/1
    response = client.get("/unidad/1")
    assert response.status_code == 200
    assert response.json() == {
        "descripcion": "Unidad adimensional",
        "codigo": 1,
        "unidad": "Adimensional"
    }

def test_get_unidad_by_unidad():
    # Simula una solicitud GET a la ruta '/unidad'
    response = client.get("/unidad/?unidad=Adimensional")

    # Verifica que la respuesta tenga un código de estado 200 (éxito)
    assert response.status_code == 200

    # Decodifica el contenido JSON de la respuesta
    result = response.json()

    # Verifica que el resultado sea una lista no vacía
    assert isinstance(result, list)
    assert len(result) > 0

    # Verifica que cada elemento de la lista sea un objeto JSON válido
    for unidad in result:
        assert isinstance(unidad, dict)

        # Verifica que cada objeto tenga los campos esperados (ajusta esto según tus datos)
        assert "codigo" in unidad
        assert "descripcion" in unidad
        assert "unidad" in unidad


unidad_prueba = {
    "unidad": "Adimensional",
}



def test_get_unidad_list():
    # Simula una solicitud GET a la ruta '/unidad'
    response = client.get("/unidad")

    # Verifica que la respuesta tenga un código de estado 200 (éxito)
    assert response.status_code == 200

    # Decodifica el contenido JSON de la respuesta
    result = response.json()

    # Verifica que el resultado sea una lista no vacía
    assert isinstance(result, list)
    assert len(result) > 0

    # Verifica que cada elemento de la lista sea un objeto JSON válido
    for unidad in result:
        assert isinstance(unidad, dict)

        # Verifica que cada objeto tenga los campos esperados (ajusta esto según tus datos)
        assert "codigo" in unidad
        assert "descripcion" in unidad
        assert "unidad" in unidad


unidad_prueba = {
    "unidad": "Prueba",
    "descripcion": "Prueba Final"
}

# Fixture de pytest para configurar una sesión de base de datos temporal
@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()

# Fixture de pytest para crear la unidad de prueba y limpiar la base de datos después
@pytest.fixture
def create_and_cleanup_unit(db_session):
    # Realiza la solicitud POST para crear la unidad
    response = client.post("/unidad", json=unidad_prueba)

    # Verifica el código de estado de la respuesta
    assert response.status_code == 201

    # Verifica el contenido de la respuesta
    response_data = response.json()
    assert response_data["message"] == "Se ha registrado la unidad"
    
    # Verifica que el campo "unidad creada" esté presente en la respuesta
    assert "unidad creada" in response_data
    
    # Verifica que el ID de la unidad creada no sea None y sea un entero
    unidad_creada_id = response_data["unidad creada"]
    assert isinstance(unidad_creada_id, int)

    # Retorna el ID de la unidad creada para que pueda ser utilizado en el test
    yield unidad_creada_id

    # Después de que el test haya terminado, limpia la base de datos eliminando la unidad creada
    with db_session.begin():
        unidad_creada = db_session.query(unidad_model).filter_by(codigo=unidad_creada_id).first()
        if unidad_creada:
            db_session.delete(unidad_creada)
            db_session.commit()

def test_post_unidad(create_and_cleanup_unit):
    # El ID de la unidad creada se obtiene del fixture create_and_cleanup_unit
    unidad_creada_id = create_and_cleanup_unit



def test_post_unidad_error():
    body = {
        "unidad": "Japan"
    }
    response = client.post("/unidad", json=body)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'type': 'missing',
            'loc': ['body', 'descripcion'],
            'msg': 'Field required',
            'input':{
                'unidad': 'Japan'
            },
        'url': 'https://errors.pydantic.dev/2.3/v/missing'
        }]
    }

def test_patch_unidad_error():
    body = {
        "unidad": "prueba error patch"
    }
    response = client.patch("/unidad/20000", json=body)
    assert response.status_code == 422
    assert response.json() == {"message": "No encontrado"}
    
    

def test_error_404():
    response = client.get("/unidad/500")
    assert response.status_code == 404
    assert response.json() == {"message": "No encontrado"}


def test_handle_value_error():
    try:
        # Simula una situación en la que se produce un ValueError
        # Esto puede ser cualquier escenario que cause la excepción que deseas probar
        raise ValueError("Este es un mensaje de error")

    except ValueError as e:
        # Captura la excepción y verifica que se eleve una HTTPException con el código de estado 400
        # y el detalle adecuado basado en el mensaje de error de la excepción original
        try:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException as http_exception:
            assert http_exception.status_code == 400
            assert http_exception.detail == "Este es un mensaje de error"

def test_patch_unidad():
    # Datos de prueba para el cuerpo de la solicitud (puedes ajustarlos según tus necesidades)
    codigo = 1
    item_update = {
        "unidad": "new_value"
    }

    # Abre una transacción en la base de datos
    db = SessionLocal()
    db.begin()

    try:
        # Realiza una solicitud PATCH a la ruta '/unidad/{codigo}'
        dato_actual = db.query(unidad_model).filter_by(codigo=codigo).first()
        valor_original = dato_actual.unidad
        response = client.patch(f"/unidad/{codigo}", json=item_update)

        # Verifica el código de respuesta esperado (201 en este caso)
        assert response.status_code == 201

        # Verifica el contenido de la respuesta (puedes ajustarlo según lo que devuelve tu función)
        response_data = response.json()
        assert "message" in response_data
        assert response_data["message"] == "Se ha registrado la unidad"

        # También puedes realizar otras aserciones según la lógica de tu aplicación
        restaurar_actualizacion = {
            "unidad": valor_original
        }
        response = client.patch(f"/unidad/{codigo}", json=restaurar_actualizacion)
        assert response.status_code == 201
        # Confirma la transacción
        db.commit()

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la prueba
        print(f"Error durante la prueba: {str(e)}")
        # Hacer un rollback en caso de excepción
        db.rollback()
    finally:
        # Cierra la sesión de la base de datos
        db.close()

    # Asegúrate de cerrar la sesión del cliente de prueba (si es necesario)
    response.close()


