from database.elasticsearch.manager import ElasticsearchDB


class ContentES(ElasticsearchDB):
    index = "content"

    def search(self, text: str):
        query = {"query": {"query_string": {"query": text}}}
        return super().search(query=query)
