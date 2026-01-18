# importing the libraries
from usecase.action_agent import interact_action_query
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    user_input = payload["prompt"]
    print("User Input:", user_input)
    response = interact_action_query(user_input)
    return response


