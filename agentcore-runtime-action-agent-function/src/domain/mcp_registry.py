# importing the libraries
import os


class MCPConfig:
    REGION_NAME = os.environ["REGION"]
    MCP_URL = os.environ["MCP_URL"]