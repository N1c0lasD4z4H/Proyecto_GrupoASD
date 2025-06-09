import os
from elasticsearch import Elasticsearch, AsyncElasticsearch
from dotenv import load_dotenv
from ssl import create_default_context

load_dotenv()

cert_path = os.getenv("CERT_PATH", "/certs/ca/ca.crt")
context = create_default_context(cafile=cert_path)

es = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER"),
        os.getenv("ELASTICSEARCH_PASSWORD"),
    ),
    ssl_context=context,
    verify_certs=True,
)

es_async = AsyncElasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER"),
        os.getenv("ELASTICSEARCH_PASSWORD"),
    ),
    ssl_context=context,
    verify_certs=True,
)
