import os

from langchain.vectorstores.azuresearch import AzureSearch
from azure.search.documents.indexes.models import (
    SemanticSettings,
    SemanticConfiguration,
    PrioritizedFields,
    SemanticField,
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchField,
)


VECTOR_STORE_ADDRESS = os.environ.get("VECTOR_STORE_ADDRESS")
VECTOR_STORE_PASSWORD = os.environ.get("VECTOR_STORE_PASSWORD")


def get_fields(embedding_function):
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embedding_function("Text")),
            vector_search_configuration="default",
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        # Additional field to store the title
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        # Additional field for filtering on document source
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        # Additional data field for last doc update
        SimpleField(
            name="last_update",
            type=SearchFieldDataType.DateTimeOffset,
            searchable=True,
            filterable=True,
        ),
    ]
    return fields


class AzureVectorStorage:
    _instance = None

    def __new__(cls, index_name, embeddings):
        if cls._instance is None:
            cls._instance = super(AzureVectorStorage, cls).__new__(cls)
            cls._instance.vector_storage = AzureSearch(
                azure_search_endpoint=VECTOR_STORE_ADDRESS,
                azure_search_key=VECTOR_STORE_PASSWORD,
                index_name=index_name,
                embedding_function=embeddings.embed_query,
                fields=get_fields(embeddings.embed_query),
                semantic_configuration_name="config",
                semantic_settings=SemanticSettings(
                    default_configuration="config",
                    configurations=[
                        SemanticConfiguration(
                            name="config",
                            prioritized_fields=PrioritizedFields(
                                title_field=SemanticField(field_name="content"),
                                prioritized_content_fields=[
                                    SemanticField(field_name="content")
                                ],
                                prioritized_keywords_fields=[
                                    SemanticField(field_name="metadata")
                                ],
                            ),
                        )
                    ],
                ),
            )
        return cls._instance

    async def add_documents(self, docs):
        ids = self.vector_storage.add_documents(documents=docs)
        return ids

    def search(self, query):
        docs = self.vector_storage.similarity_search(
            query=query,
            k=3,
            search_type="hybrid",
        )
        return docs
