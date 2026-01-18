output "agent_core_agent_runtime_id" {
  value = aws_bedrockagentcore_agent_runtime.mcp.agent_runtime_id
}

output "agent_core_agent_runtime_arn" {
  value = aws_bedrockagentcore_agent_runtime.mcp.agent_runtime_arn
}

output "agent_core_agent_runtime_endpoint_arn" {
  value = aws_bedrockagentcore_agent_runtime_endpoint.endpoint.agent_runtime_endpoint_arn
}

output "endpoint_name" {
  value = "${var.environment}_${var.component_name}_bedrockagentruntimeendpointv1"
}