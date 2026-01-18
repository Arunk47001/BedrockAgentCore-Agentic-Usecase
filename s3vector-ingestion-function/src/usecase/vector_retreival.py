# importing libraries
from infra.s3.s3_vector_store import S3VectorStoreEngine


def retrieval(query:str):
    try:
        s3_vector_store = S3VectorStoreEngine()
        response=s3_vector_store.retrieval_document(query=query, top_k=3)
    except Exception as err:
        print(err)
        raise ValueError("Error in retrieval process")
