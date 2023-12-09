from fastapi.testclient import TestClient
from main import app  # Importa la instancia de la aplicación desde el archivo principal de la aplicación
from fastapi.responses import JSONResponse
from models.unidad_espacial_referencia_dt import UnidadEspacialReferenciaModel
from pydantic import ValidationError
import pytest
from config.database import SessionLocal
from fastapi.exceptions import HTTPException

client = TestClient(app)  # Crea un cliente de prueba para la aplicación