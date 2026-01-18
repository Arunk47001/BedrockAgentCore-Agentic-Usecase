# importing the libraries
import uuid
import json

from domain.abstract.vector_store_repo import VectorStoreEngineRepo
from domain.vector_config import VectorConfig
from infra.s3.s3vector import S3VectorConnect
from infra.bedrock.bedrock_embedding import embedding

class S3VectorStoreEngine(VectorStoreEngineRepo):
    def __init__(self):
        self.src_bucket = VectorConfig.vector_bucket
        self.index_name = VectorConfig.index_name

    def retrieval_document(self, query:str, top_k:int):
        try:
            s3 = S3VectorConnect(bucket_name=self.src_bucket)
            vector = embedding(query)
            response_body = json.loads(vector["body"].read())
            response = s3.s3vector_query_vector(index_name=self.index_name, query_vector=response_body["embedding"], top_k=top_k)
            return json.dumps(response["vectors"], indent=2)
        except Exception as err:
            print(err)
            raise ValueError("Error in retrieving document from vector store")
