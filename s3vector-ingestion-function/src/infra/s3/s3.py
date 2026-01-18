# importing the libraries
import os
import boto3


class S3Connect:
    def __init__(self, bucket_name: str):
        self.src_bucket = bucket_name

    def s3_put(self, response: str, s3_path: str):
        s3_resource = boto3.resource('s3', region_name=os.environ["REGION"])
        s3_resource.Bucket(self.src_bucket).put_object(Key=s3_path, Body=response)

    def s3_get(self, src_file: str) -> str:
        s3_client = boto3.client('s3', region_name=os.environ["REGION"])
        input_content_object = s3_client.get_object(Bucket=self.src_bucket, Key=src_file)['Body'].read()
        return input_content_object

    def s3_delete(self, src_file: str):
        s3_client = boto3.client('s3', region_name=os.environ["REGION"])
        s3_client.delete_object(Bucket=self.src_bucket, Key=src_file)

    def s3_list_pdfs(self, prefix: str = None) ->[]:
        s3_client = boto3.client('s3', region_name=os.environ["REGION"])
        pdf_files = []
        kwargs = {"Bucket": self.src_bucket}
        if prefix:
            kwargs["Prefix"] = prefix
        while True:
            response = s3_client.list_objects_v2(**kwargs)

            for obj in response.get("Contents", []):
                if obj["Key"].lower().endswith(".pdf"):
                    pdf_files.append(obj["Key"])

            # Check if there are more pages of results
            if response.get("IsTruncated"):
                kwargs["ContinuationToken"] = response["NextContinuationToken"]
            else:
                break

        return pdf_files

    def s3_uploadfileobj(self, src_file, src_name: str):
        s3_client = boto3.client('s3', region_name = os.environ['REGION'])
        s3_client.upload_fileobj(src_file,self.src_bucket, src_name)
