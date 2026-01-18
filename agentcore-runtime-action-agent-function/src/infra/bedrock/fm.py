# importing the libraries
from strands.models import BedrockModel


def get_bedrock_model() -> BedrockModel:
    bedrock_model = BedrockModel(
        model_id='us.anthropic.claude-haiku-4-5-20251001-v1:0',
        temperature=0.5,
        region_name='us-east-1',
    )
    return bedrock_model