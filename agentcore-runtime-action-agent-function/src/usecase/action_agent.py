# importing the libraries
import os
from strands import Agent, tool
from mcp import ClientSession
from strands.tools.mcp.mcp_client import MCPClient
import boto3
from domain.streamable_http_sigv4 import streamablehttp_client_with_sigv4
from domain.prompt_registry import PromptConfig
from infra.bedrock.fm import get_bedrock_model
from domain.mcp_registry import MCPConfig

os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

def create_streamable_http_transport_sigv4(
    mcp_url: str, service_name: str, region: str
):
    """
    Create a streamable HTTP transport with AWS SigV4 authentication.

    This function creates an MCP client transport that uses AWS Signature Version 4 (SigV4)
    to authenticate requests. This is necessary because standard MCP clients don't natively
    support AWS IAM authentication, and this bridges that gap.

    Args:
        mcp_url (str): The URL of the MCP gateway endpoint
        service_name (str): The AWS service name for SigV4 signing (typically "bedrock-agentcore")
        region (str): The AWS region where the gateway is deployed

    Returns:
        StreamableHTTPTransportWithSigV4: A transport instance configured for SigV4 auth
    """
    # Get AWS credentials from the current boto3 session
    # These credentials will be used to sign requests with SigV4
    session = boto3.Session()
    credentials = session.get_credentials()

    # Create and return the custom transport with SigV4 signing capability
    return streamablehttp_client_with_sigv4(
        url=mcp_url,
        credentials=credentials,
        service=service_name,
        region=region,
    )

def get_full_tools_list(client):
    more_tools = True
    tools = []
    pagination_token = None
    while more_tools:
        tmp_tools = client.list_tools_sync(pagination_token=pagination_token)
        tools.extend(tmp_tools)
        if tmp_tools.pagination_token is None:
            more_tools = False
        else:
            more_tools = True
            pagination_token = tmp_tools.pagination_token
    return tools

def call_tool_sync(client, tool_id,tool_name, parameters=None):
    # Call the tool (no pagination argument supported)
    response = client.call_tool_sync(
        tool_use_id=tool_id,
        name=tool_name,
        arguments=parameters
    )

    # Extract output content
    if hasattr(response, "results") and response.results:
        return response.results
    elif hasattr(response, "output") and response.output:
        return response.output
    elif hasattr(response, "content"):
        return response.content
    else:
        return response  # fallback


@tool
async def interact_city_action_tool(name: str, arguments: dict):
    region = MCPConfig.REGION_NAME
    mcp_url = MCPConfig.MCP_URL
    mcp_client = MCPClient(
        lambda: create_streamable_http_transport_sigv4(mcp_url,service_name="bedrock-agentcore", region=region))

    with mcp_client:
        tools = get_full_tools_list(mcp_client)
        print(f"Found the following tools: {[tool.tool_name for tool in tools]}")
        print(f"Tool name: {tools[0].tool_name}")
        print(f"given name: {name}")
        print(f"given arguments: {arguments}")

def interact_action_query(query: str):
    region = MCPConfig.REGION_NAME
    mcp_url = MCPConfig.MCP_URL
    mcp_client = MCPClient(
        lambda: create_streamable_http_transport_sigv4(mcp_url,service_name="bedrock-agentcore", region=region))

    with mcp_client:
        tools = get_full_tools_list(mcp_client)
        action_agent = Agent(
            model=get_bedrock_model(),
            system_prompt=PromptConfig.action_prompt,
            tools=tools,
        )
        response = action_agent(query)
        return str(response)






