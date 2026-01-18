# importing the libraries
import os


class AgentRegistry:
    action_agent_arn = os.environ['ACTION_AGENT_ARN']
    rag_agent_arn = os.environ['RAG_AGENT_ARN']
    region = os.environ['REGION']