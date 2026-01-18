
resource "aws_bedrockagentcore_gateway" "gateway" {
  name = "${var.environment}-${var.gateway_name}-gt"
  role_arn           = aws_iam_role.gateway_iam_role.arn
  authorizer_type = "AWS_IAM"
  protocol_type = "MCP"
  tags =var.tags
}



######################IAM Roles################
resource "aws_iam_role" "gateway_iam_role" {
  name = "${var.environment}-${var.component_name}-gateway-role"
  assume_role_policy = jsonencode({
              "Version": "2012-10-17",
              "Statement": [{
                      "Effect": "Allow",
                      "Principal": {
                          "Service": [
                              "bedrock-agentcore.amazonaws.com"
                          ]
                      },
                      "Action": "sts:AssumeRole"
                  }
              ]
          })
}

##################IAM Policy#####################
resource "aws_iam_role_policy" "gateway_iam_policy" {
  name = "${var.environment}-${var.component_name}-gateway-policy-for-${var.region}"
  role = aws_iam_role.gateway_iam_role.name
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudwatchLogs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "logs:CreateLogStream"
            ],
            "Resource": ["*"]
        },
      {
         Effect : "Allow",
        Resource : ["arn:aws:bedrock:${var.region}::foundation-model/*"],
        Action: [
          "bedrock:*",
        ]
      },
      {
    "Sid": "CreateBedrockAgentCoreIdentityServiceLinkedRolePermissions",
    "Effect": "Allow",
    "Action": "iam:CreateServiceLinkedRole",
    "Resource": "arn:aws:iam::*:role/aws-service-role/runtime-identity.bedrock-agentcore.amazonaws.com/AWSServiceRoleForBedrockAgentCoreRuntimeIdentity",
    "Condition": {
        "StringEquals": {
            "iam:AWSServiceName": "runtime-identity.bedrock-agentcore.amazonaws.com"
        }
    }
},
      {
    "Sid": "GetAgentAccessToken",
    "Effect": "Allow",
    "Action": [
        "bedrock-agentcore:GetWorkloadAccessToken",
        "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
        "bedrock-agentcore:GetWorkloadAccessTokenForUserId"
    ],
    "Resource": [
        "*"
    ]
},
      {
        "Sid": "AllowLambdaAccess",
        "Effect": "Allow",
        "Action": [
           "agent-credential-provider:*",
           "iam:PassRole",
           "lambda:InvokeFunction"
        ],
        "Resource": [
           "*"
        ]
      }
    ]
})
}