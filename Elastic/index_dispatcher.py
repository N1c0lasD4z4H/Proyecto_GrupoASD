from Elastic.elastic_client import es
from pydantic import BaseModel
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def send_document(index_name: str, doc_id: str, document: Union[BaseModel, dict]):
    """
    Envía cualquier documento validado a Elasticsearch.
    """
    try:
        payload = document.model_dump() if isinstance(document, BaseModel) else document
        await es.index(index=index_name, id=doc_id, document=payload)
        logger.info(f"Indexed into {index_name}: {doc_id}")
    except Exception as e:
        logger.error(f"Indexing error: {str(e)}")
        raise
