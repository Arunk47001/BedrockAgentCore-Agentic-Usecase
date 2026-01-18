# importing the libraries
import os
from strands import Agent, tool
from mcp import ClientSession
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

@tool
async def docs_rag_tool(name: str, arguments: dict) -> str:
    region = MCPConfig.REGION_NAME
    mcp_url = MCPConfig.MCP_URL
    try:
        async with create_streamable_http_transport_sigv4(mcp_url,service_name="bedrock-agentcore", region=region) as (
                    read_stream,
                    write_stream,
                    _,
            ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(name=name, arguments=arguments)
                return result.content[0].text

    finally:
        # Best-effort shutdown; ignore 404s from the gateway
        try:
            if session is not None:
                await session.close()
        except Exception:
            pass
        try:
            if write_stream is not None:
                await write_stream.aclose()
            if read_stream is not None:
                await read_stream.aclose()
        except Exception:
            pass


def docs_rag_agent(query:str):
    try:
        print("Invoking RAG agent with query:", query)
        rag_agent = Agent(
            model=get_bedrock_model(),
            system_prompt=PromptConfig.rag_prompt,
            tools=[docs_rag_tool],
        )
        response = rag_agent(query)
        return str(response)
    except Exception as e:
        return f"Error occurred while processing the RAG agent: {str(e)}"

