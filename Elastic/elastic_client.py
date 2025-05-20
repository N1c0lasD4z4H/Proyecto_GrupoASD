from elasticsearch import Elasticsearch 
from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv
from ssl import create_default_context


context = create_default_context(cafile=r"C:\ELK\elasticsearch\config\certs\http_ca.crt")
load_dotenv()

es = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")], 
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER"),
        os.getenv("ELASTICSEARCH_PASSWORD")
    ),
    verify_certs=True
    
)
es_async = AsyncElasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    basic_auth=(os.getenv("ELASTICSEARCH_USER"), os.getenv("ELASTICSEARCH_PASSWORD")),
    ssl_context=context,
    verify_certs=True
)