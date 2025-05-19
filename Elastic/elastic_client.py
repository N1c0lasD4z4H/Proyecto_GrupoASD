from elasticsearch import Elasticsearch  # ✅ usa cliente síncrono
import os
from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")], 
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER"),
        os.getenv("ELASTICSEARCH_PASSWORD")
    ),
    ca_certs="C:\\ELK\\elasticsearch\\config\\certs\\http_ca.crt",
    verify_certs=True
)
