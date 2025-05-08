import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel
from typing import Dict
import logging
from Elastic.index_dispatcher import send_document  # Ajusta esto a tu estructura de imports

# Mock Model para pruebas
class MockModel(BaseModel):
    name: str
    value: int

# Fixture para el mock de Elasticsearch
@pytest.fixture
def mock_es():
    with patch('Elastic.index_dispatcher.es') as mock:  # Ruta corregida
        mock.index = AsyncMock()
        yield mock

# Fixture para capturar logs
@pytest.fixture
def caplog(caplog):
    caplog.set_level(logging.INFO)
    return caplog


@pytest.mark.asyncio
async def test_send_document_with_model(mock_es, caplog):
    """Test enviar documento con modelo Pydantic"""
    test_model = MockModel(name="test", value=123)
    
    # Versión moderna (Pydantic v2)
    expected_payload = test_model.model_dump()
    
    await send_document("test_index", "doc1", test_model)
    
    mock_es.index.assert_awaited_once_with(
        index="test_index",
        id="doc1",
        document=expected_payload
    )
    assert "Indexed into test_index: doc1" in caplog.text  # f-string eliminado

@pytest.mark.asyncio
async def test_send_document_with_dict(mock_es, caplog):
    """Test enviar documento con diccionario"""
    # Arrange
    test_dict = {"key": "value", "num": 42}
    
    # Act
    await send_document("test_index", "doc2", test_dict)
    
    # Assert
    mock_es.index.assert_awaited_once_with(
        index="test_index",
        id="doc2",
        document=test_dict
    )
    assert "Indexed into test_index: doc2" in caplog.text  # f-string eliminado

@pytest.mark.asyncio
async def test_send_document_error_handling(mock_es, caplog):
    """Test manejo de errores al enviar documento"""
    # Arrange
    test_dict = {"key": "value"}
    mock_es.index.side_effect = Exception("Elasticsearch error")
    
    # Act/Assert
    with pytest.raises(Exception) as exc_info:
        await send_document("test_index", "doc3", test_dict)
    
    assert str(exc_info.value) == "Elasticsearch error"
    assert "Indexing error: Elasticsearch error" in caplog.text

@pytest.mark.asyncio
async def test_logging_on_success_and_error(mock_es, caplog):
    """Test que verifica los mensajes de log correctos"""
    # Test éxito
    await send_document("test_index", "doc4", {"a": 1})
    assert "Indexed into test_index: doc4" in caplog.text
    
    # Test error
    mock_es.index.side_effect = Exception("Failed")
    with pytest.raises(Exception):
        await send_document("test_index", "doc5", {"a": 1})
    assert "Indexing error: Failed" in caplog.text