output "function_name" {
  value = aws_lambda_function.lambda_function.function_name
}

output "gateway_url" {
  value = aws_bedrockagentcore_gateway.gateway.gateway_url
}

output "gateway_arn" {
  value = aws_bedrockagentcore_gateway.gateway.gateway_arn
}