output "agent_core_agent_runtime_id" {
  value = aws_bedrockagentcore_agent_runtime.agent.agent_runtime_id
}

output "agent_core_agent_runtime_arn" {
  value = aws_bedrockagentcore_agent_runtime.agent.agent_runtime_arn
}

output "agent_core_endpoint_arn" {
  value = aws_bedrockagentcore_agent_runtime_endpoint.endpoint.agent_runtime_endpoint_arn
}