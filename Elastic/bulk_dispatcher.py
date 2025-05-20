from elasticsearch import helpers
from Elastic.elastic_client import es
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
