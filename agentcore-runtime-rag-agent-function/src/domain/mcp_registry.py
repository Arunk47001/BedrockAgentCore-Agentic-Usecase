# importing the libraries
import os


class MCPConfig:
    REGION_NAME = os.environ["REGION"]
    AGENT_ARN = os.environ["AGENT_ARN"]
    ENCODED_ARN = AGENT_ARN.replace(":", "%3A").replace("/", "%2F")
    MCP_URL = f"https://bedrock-agentcore.{REGION_NAME}.amazonaws.com/runtimes/{ENCODED_ARN}/invocations?qualifier={os.environ['QUALIFIER']}"