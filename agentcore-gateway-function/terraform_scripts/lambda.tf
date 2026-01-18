data "aws_ecr_image" "image" {
  repository_name = var.repository_name
  image_tag = var.image_tag
}

data "aws_caller_identity" "current" {}


resource "aws_lambda_function" "lambda_function" {
  function_name = "${var.environment}-${var.component_name}-lambda"
  image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.repository_name}@${data.aws_ecr_image.image.image_digest}"
  package_type  = "Image"
  role          = aws_iam_role.iam_role.arn
  timeout       = var.lambda_timeout
  environment {
    variables = {
      env = var.environment
      REGION =var.region
      access = var.access
    }
}
  memory_size = var.lambda_memory
  tags =  merge(var.tags, {Stage = var.environment})
}

resource "aws_iam_role" "iam_role" {
  name = "${var.environment}-${var.component_name}-role"
  assume_role_policy = jsonencode({
              "Version": "2012-10-17",
              "Statement": [{
                      "Effect": "Allow",
                      "Principal": {
                          "Service": [
                              "lambda.amazonaws.com"
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

            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
               "ssm:GetParameter",
              "ssm:DescribeParameters",
              "ssm:GetParametersByPath",
              "ssm:GetParameters"
            ],
            "Resource": ["arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/*"]
        }
    ]
})
}