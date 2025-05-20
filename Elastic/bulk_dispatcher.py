from elasticsearch import helpers
from Elastic.elastic_client import es
from elasticsearch.helpers import async_bulk
import logging

logger = logging.getLogger(__name__)

def send_bulk_documents(index_name: str, documents: list):
    try:
        actions = [{"_index": index_name, "_source": doc} for doc in documents]
        helpers.bulk(es, actions)
        logger.info(f"[✔] {len(actions)} documentos enviados al índice '{index_name}'")
    except Exception as e:
        logger.error(f"[❌] Error enviando documentos: {str(e)}")
        raise
async def async_send_bulk_documents(index_name: str, documents: list):

    try:
        actions = [{"_index": index_name, "_source": doc} for doc in documents]
        success, failed = await async_bulk(es, actions)
        logger.info(f"[✔] Documentos enviados: {len(success)}, Fallidos: {len(failed)} al índice '{index_name}'")
    except Exception as e:
        logger.error(f"[❌] Error enviando documentos (async): {str(e)}", exc_info=True)
        raise