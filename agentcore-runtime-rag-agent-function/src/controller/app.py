# importing the libraries
from applications.rag_assistant import docs_rag_agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    user_input = payload["prompt"]
    print("User Input:", user_input)
    response = interact_rag_agent(user_input)
    return response


