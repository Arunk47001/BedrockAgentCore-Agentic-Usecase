# importing the libraries
import os
from strands import Agent, tool
from infra.bedrock.fm import get_bedrock_model
from domain.prompt_registry import PromptConfig
from domain.agent_tools import call_action_agent, call_rag_agent

os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"
os.environ["BYPASS_TOOL_CONSENT"] = "true"


orche_agent = Agent(
        model=get_bedrock_model(),
        system_prompt=PromptConfig.supervisor_promptv1,
        tools=[call_action_agent, call_rag_agent]
    )




