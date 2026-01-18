# importing the libraries
import os
import boto3


class S3VectorConnect:
    def __init__(self, bucket_name: str):
        self.src_bucket = bucket_name

    def s3vector_create_index(self, index_name: str):
        s3vectorclient = boto3.client('s3vectors', region_name=os.environ["REGION"])
        s3vectorclient.create_index(
            vectorBucketName=self.src_bucket,
            indexName=index_name,
            dataType='float32',
            dimension=1024,
            distanceMetric='euclidean',
        metadataConfiguration = {
            "nonFilterableMetadataKeys": [
                "text"
            ]
        }
        )

    def s3vector_get_index(self, index_name: str):
        s3vectorclient = boto3.client('s3vectors', region_name=os.environ["REGION"])
        response = s3vectorclient.get_index(
            vectorBucketName=self.src_bucket,
            indexName=index_name
        )
        return response

    def s3vector_delete_index(self, index_name: str):
        s3vectorclient = boto3.client('s3vectors', region_name=os.environ["REGION"])
        s3vectorclient.delete_index(
            vectorBucketName=self.src_bucket,
            indexName=index_name
        )

    def s3vector_put_vector(self, index_name: str, vector_data: list):
        s3vectorclient = boto3.client('s3vectors', region_name=os.environ["REGION"])
        s3vectorclient.put_vectors(
            vectorBucketName=self.src_bucket,
            indexName=index_name,
            vectors= vector_data
        )

    def s3vector_query_vector(self, index_name: str, query_vector: list, top_k: int):
        s3vectorclient = boto3.client('s3vectors', region_name=os.environ["REGION"])
        response = s3vectorclient.query_vectors(
            vectorBucketName=self.src_bucket,
            indexName=index_name,
            queryVector={'float32': query_vector},
            topK=top_k,
            returnMetadata=True
        )
        return response

