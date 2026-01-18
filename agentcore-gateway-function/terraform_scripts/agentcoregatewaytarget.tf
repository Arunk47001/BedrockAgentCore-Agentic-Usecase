
resource "aws_bedrockagentcore_gateway_target" "target" {
  name               =  "${var.environment}-${var.gateway_name}-target"
  gateway_identifier = aws_bedrockagentcore_gateway.gateway.gateway_id

  credential_provider_configuration {
    gateway_iam_role {}
  }

  target_configuration {
    mcp {
      lambda {
        lambda_arn = aws_lambda_function.lambda_function.arn
        tool_schema {
          inline_payload {
            name        = "get_asset_tool"
            description = "tool to get the asset info"
            input_schema {
              type        = "object"
              description = "asset identifier"

              property {
                name        = "streetAssetId"
                type        = "string"
                description = "asset identifier"
                required    = true
              }
            }
          }
          inline_payload {
            name        = "get_switch_tool"
            description = "tool to get the switch info"
            input_schema {
              type        = "object"
              description = "switch identifier"

              property {
                name        = "lumAssetId"
                type        = "string"
                description = "asset identifier"
                required    = true
              }
              property {
                name       = "startDate"
                type        = "string"
                description = "startdate for switch data"
                required    = true
              }
              property {
                name       = "endDate"
                type        = "string"
                description = "enddate for switch data"
                required    = true
              }
            }
          }
        }
      }
    }
  }
}