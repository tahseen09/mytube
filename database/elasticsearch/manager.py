from typing import Optional
from uuid import uuid4
from elasticsearch import Elasticsearch

from content.constants import ELASTICSEARCH_DOCKER_BASE_URL


class ElasticsearchDB:
    url: str = ELASTICSEARCH_DOCKER_BASE_URL
    index: str = None

    def __init__(self, url: Optional[str] = None, index: Optional[str] = None) -> None:
        self.url = url or self.url
        self.index = index or self.index
        self.db = Elasticsearch([self.url])

    def insert(self, document: dict):
        return self.db.create(index=self.index, id=str(uuid4()), body=document)

    def search(self, query: dict):
        return self.db.search(index=self.index, body=query)
