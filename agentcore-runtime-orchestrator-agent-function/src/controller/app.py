# importing the libraries
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from applications.orchestrator_agent import orche_agent

app = BedrockAgentCoreApp()


@app.entrypoint
def strands_agent_bedrock_streaming(payload):
    """
    Entrypoint for the Bedrock AgentCore application.
    """
    user_input = payload["prompt"]
    print("User Input:", user_input)
    response = orche_agent(user_input)
    return response

