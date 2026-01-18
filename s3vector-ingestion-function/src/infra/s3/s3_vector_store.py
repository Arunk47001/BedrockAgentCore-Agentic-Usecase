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

    def create_index(self):
        s3 = S3VectorConnect(bucket_name=self.src_bucket)
        try:
            s3.s3vector_get_index(index_name=self.index_name)
            s3.s3vector_delete_index(index_name=self.index_name)
        except Exception:
            print("Already index not exists, creating new index")
        s3.s3vector_create_index(index_name=self.index_name)

    def add_document(self, documents):
        try:
            s3 = S3VectorConnect(bucket_name=self.src_bucket)
            for doc in documents:
                vector = embedding(doc.page_content)
                response_body = json.loads(vector["body"].read())
                meta_data =[
                    {
                        "key": f"{uuid.uuid4()}",
                        "data": {"float32": response_body["embedding"]},
                        "metadata": {"text": doc.page_content}
                    }
                ]
                s3.s3vector_put_vector(index_name=self.index_name, vector_data=meta_data)
        except Exception as err:
            print(err)
            raise ValueError("Error in adding document to vector store")

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
