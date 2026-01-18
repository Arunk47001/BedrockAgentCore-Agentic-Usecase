# importing libraries
from infra.s3.s3_text_splitter import S3TextSplitterEngine
from infra.s3.s3_vector_store import S3VectorStoreEngine


def ingestion():
    try:
        s3_text_splitter = S3TextSplitterEngine()
        s3_vector_store = S3VectorStoreEngine()
        s3_vector_store.create_index()
        documents = s3_text_splitter.list_all_documents()
        for doc in documents:
            chunks = s3_text_splitter.chunking_data_split(doc)
            s3_vector_store.add_document(chunks)
    except Exception as err:
        print(err)
        raise ValueError("Error in ingestion process")
