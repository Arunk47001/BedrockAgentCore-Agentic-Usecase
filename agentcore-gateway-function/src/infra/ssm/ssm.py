# importing the libraries
import logging
import boto3
import json

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SsmConnect:
    def __init__(self, name):
        self.parameter_name = name

    def get_secret(self):
        ssm_client = boto3.client('ssm', region_name='eu-central-1')
        try:
            response = ssm_client.get_parameter(
                Name=self.parameter_name,
                WithDecryption=True
            )
            parameter_value = response['Parameter']['Value']
            return json.loads(parameter_value)
        except:
            raise ValueError("Credentials not found")
