
data "aws_caller_identity" "current" {}


resource "aws_bedrockagentcore_agent_runtime" "agent" {
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
    ACTION_AGENT_ARN  = var.action_agent_arn
    RAG_AGENT_ARN     = var.rag_agent_arn
  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  protocol_configuration {
    server_protocol = "HTTP"
  }
  tags =var.tags
}

resource "aws_bedrockagentcore_agent_runtime_endpoint" "endpoint" {
  name             = "${var.environment}_orchestrator_runtimeendpointversion9"
  agent_runtime_id = aws_bedrockagentcore_agent_runtime.agent.agent_runtime_id
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
      { "Effect": "Allow",
        "Action": [ "sts:GetCallerIdentity" ],
        "Resource": "*"
      },
      {
         Effect : "Allow",
        Resource : ["arn:aws:bedrock:*::foundation-model/*", "arn:aws:bedrock:*:${data.aws_caller_identity.current.account_id}:inference-profile/*"],
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
    "Sid": "XRayPermissions",
    "Effect": "Allow",
    "Action": [
        "xray:PutTraceSegments"
    ],
    "Resource": [
        "*"
    ]
},

      {
    "Sid": "GetAgentAccessToken",
    "Effect": "Allow",
    "Action": [
        "bedrock-agentcore:*"
    ],
    "Resource": [
        "*"
    ]
}
    ]
})
}