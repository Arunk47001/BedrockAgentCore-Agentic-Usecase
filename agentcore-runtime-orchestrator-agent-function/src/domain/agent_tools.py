# importing the libraries
from strands import tool
import os
from infra.agentcoreruntime.invoke_runtime import invoke_agent_with_boto3
from domain.agent_registry import AgentRegistry
from domain.insight_registry import InsightsConfig

os.environ["BYPASS_TOOL_CONSENT"] = "true"

@tool
def call_rag_agent(user_query)-> str:
    """
    Args:
        user_query (str): The user's query to be processed by the RAG agent
    Returns:
        str: The response from the RAG agent or an error message
    """
    try:
        rag_agent_arn = AgentRegistry.rag_agent_arn
        result = invoke_agent_with_boto3(rag_agent_arn, user_query=user_query)
        InsightsConfig.rag_insight = str(result)
        return str(result)
    except Exception as e:
        return f"Error invoking RAG agent: {str(e)}"

@tool
def call_action_agent(user_query)->str:
    """
    Args:
        user_query (str): The user's query to be processed by the Action agent
    Returns:
        str: The response from the Action agent or an error message
    """
    try:
        action_agent_arn = AgentRegistry.action_agent_arn
        result = invoke_agent_with_boto3(action_agent_arn, user_query=user_query)
        InsightsConfig.action_insight = str(result)
        return str(result)
    except Exception as e:
        return f"Error invoking Action agent: {str(e)}"