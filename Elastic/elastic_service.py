
from Elastic.elastic_client import es

def index_data(index_name: str, document_id: str, data: dict):
    """
    Indexa un documento en Elasticsearch.
    :param index_name: Nombre del índice.
    :param document_id: ID único para el documento.
    :param data: Diccionario con el contenido a indexar.
    """
    return es.index(index=index_name, id=document_id, document=data)
