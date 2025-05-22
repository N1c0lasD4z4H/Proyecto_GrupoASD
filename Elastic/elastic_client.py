import os
from elasticsearch import Elasticsearch, AsyncElasticsearch

# Detecta si está corriendo en GitHub Actions (o en CI)
IS_CI = os.getenv("CI", "false").lower() == "true"

if IS_CI:
    # En CI usamos conexión simple sin TLS ni certificados
    es = Elasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")],
        verify_certs=False,
        ssl_show_warn=False,
    )
    es_async = AsyncElasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")],
        verify_certs=False,
        ssl_show_warn=False,
    )
else:
    from ssl import create_default_context
    context = create_default_context(cafile=r"C:\ELK\elasticsearch\config\certs\http_ca.crt")

    es = Elasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_URL")],
        basic_auth=(
            os.getenv("ELASTICSEARCH_USER"),
            os.getenv("ELASTICSEARCH_PASSWORD")
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
