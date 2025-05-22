from elasticsearch import helpers
from Elastic.elastic_client import es
from elasticsearch.helpers import async_bulk
import logging
import hashlib

logger = logging.getLogger(__name__)

def generate_document_id(doc: dict) -> str:
    """
    Genera un ID único para el documento basado en sus valores clave.
    Respeta la lógica actual de `username`, `repository.name`, etc.
    """
    try:
        if "username" in doc and "repository" in doc and "name" in doc["repository"]:
            base = f"{doc['username']}_{doc['repository']['name']}"
        elif "repository" in doc and isinstance(doc["repository"], dict):
            repo = doc["repository"]
            base = f"{repo.get('owner', '')}_{repo.get('name', '')}_{doc.get('number', '')}"
        else:
            base = str(doc)

        return hashlib.md5(base.encode("utf-8")).hexdigest()
    except Exception as e:
        logger.warning(f"[!] No se pudo generar ID para doc: {e}")
        return hashlib.md5(str(doc).encode("utf-8")).hexdigest()

def send_bulk_documents(index_name: str, documents: list):
    """
    Envía documentos al índice especificado usando Elasticsearch Bulk API.
    Mantiene todos los datos enviados en los documentos originales.
    """
    try:
        actions = []
        for doc in documents:
            # Si el documento ya incluye `_id`, úsalo. Si no, genera uno automáticamente.
            if isinstance(doc, dict) and "_id" in doc:
                actions.append({"_index": index_name, "_id": doc["_id"], "_source": doc})
            else:
                doc_id = generate_document_id(doc)
                actions.append({"_index": index_name, "_id": doc_id, "_source": doc})

        # Envío en bloque con helpers.bulk
        helpers.bulk(es, actions)
        logger.info(f"[✔] {len(actions)} documentos enviados al índice '{index_name}'")
    except Exception as e:
        logger.error(f"[❌] Error enviando documentos: {str(e)}", exc_info=True)
        raise

async def async_send_bulk_documents(index_name: str, documents: list):
    """
    Versión asíncrona para enviar documentos al índice.
    """
    try:
        actions = []
        for doc in documents:
            if isinstance(doc, dict) and "_id" in doc:
                actions.append({"_index": index_name, "_id": doc["_id"], "_source": doc})
            else:
                doc_id = generate_document_id(doc)
                actions.append({"_index": index_name, "_id": doc_id, "_source": doc})

        # Envío asíncrono en bloque
        success_count, _ = await async_bulk(es, actions, raise_on_error=False)
        logger.info(f"[✔] Documentos enviados exitosamente: {success_count} al índice '{index_name}'")
    except Exception as e:
        logger.error(f"[❌] Error enviando documentos (async): {str(e)}", exc_info=True)
        raise
