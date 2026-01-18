
data "aws_caller_identity" "current" {}


resource "aws_bedrockagentcore_agent_runtime" "mcp" {
  agent_runtime_name = "${var.environment}_${var.component_name}_bedrockagentruntime"
  role_arn           = aws_iam_role.iam_role.arn

  agent_runtime_artifact {
    container_configuration {
      container_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.repository_name}:${var.image_tag}"
    }
  }

  environment_variables = {
    ENV       =  var.environment
    REGION    = var.region
    VECTOR_BUCKET = var.vector_bucket_name
    VECTOR_INDEX_NAME = var.vector_index_name

  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  protocol_configuration {
    server_protocol = "MCP"
  }
  tags =var.tags
}

resource "aws_bedrockagentcore_agent_runtime_endpoint" "endpoint" {
  name             = "${var.environment}_${var.component_name}_bedrockagentruntimeendpointv1"
  agent_runtime_id = aws_bedrockagentcore_agent_runtime.mcp.agent_runtime_id
  description      = "Endpoint for agent runtime communication"
}

######################IAM Roles################
resource "aws_iam_role" "iam_role" {
  name = "${var.environment}-${var.component_name}-role"
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
resource "aws_iam_role_policy" "iam_policy" {
  name = "${var.environment}-${var.component_name}-policy-for-${var.region}"
  role = aws_iam_role.iam_role.name
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
        Resource : ["*"],
        Action: [
          "s3vectors:*",
        ]

      },
      {
         Effect : "Allow",
        Resource : ["arn:aws:bedrock:${var.region}::foundation-model/*"],
        Action: [
          "bedrock:*",
        ]
      },
        {
            "Sid": "LambdaVPCPermission"
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:AttachNetworkInterface",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs"
            ],
            "Resource": ["*"]
        },
      {
        Effect : "Allow",
        Resource : "arn:aws:ecr:${var.region}:${data.aws_caller_identity.current.account_id}:repository/*"
        Action : [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
      },
       {
        Effect = "Allow"
        Action = "ecr:GetAuthorizationToken"
        Resource = "*"
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
}
    ]
})
}