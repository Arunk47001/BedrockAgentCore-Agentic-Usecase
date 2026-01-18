# importing the libraries
import os
import json
import boto3


def embedding(input_text: str):
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=os.environ["REGION"])
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": input_text})
        )
        return response
    except Exception as err:
        print(err)
        raise ValueError("Error in generating embeddings from Bedrock")
