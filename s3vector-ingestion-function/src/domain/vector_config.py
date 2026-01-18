import os


class VectorConfig:
    vector_bucket: str = os.environ["VECTOR_BUCKET"]
    index_name: str = os.environ["VECTOR_INDEX_NAME"]
    src_bucket: str = os.environ["SOURCE_BUCKET"]