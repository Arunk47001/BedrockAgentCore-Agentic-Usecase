# importing the libraries
from usecase.asset_info import get_asset_tool
from usecase.switching_info import get_switch_tool


def etl_method(event, context):
    toolName = context.client_context.custom['bedrockAgentCoreToolName']
    print(context.client_context)
    print(event)
    print(f"Original toolName: , {toolName}")
    delimiter = "___"
    if delimiter in toolName:
        toolName = toolName[toolName.index(delimiter) + len(delimiter):]
    if toolName == 'get_asset_tool':
        print("Invoking get_asset_tool with assetId:", event['streetAssetId'])
        return get_asset_tool(event['streetAssetId'])
    if toolName == 'get_switch_tool':
        print("Invoking get_switch_tool with parameters:", event)
        return get_switch_tool(event['lumAssetId'], event['startDate'], event['endDate'])
    else:
        return {'statusCode': 200, 'body': "Other tools can be implemented here."}
