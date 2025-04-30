from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

es = AsyncElasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")], 
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER"),
        os.getenv("ELASTICSEARCH_PASSWORD")
    ),
    ca_certs="C:\ELK\elasticsearch\config\certs\http_ca.crt",
    verify_certs=True
)

