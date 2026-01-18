resource "aws_ecr_repository" "chatbot-api" {
  name = "${var.common-chatbot-api}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}


resource "aws_ecr_repository" "common-server" {
  name = "${var.common-server}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}


resource "aws_ecr_repository" "common-agent" {
  name = "${var.common-agent}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}


resource "aws_ecr_repository" "api-gateway" {
  name = "${var.api-gateway}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_repository" "api-agent" {
  name = "${var.api-agent}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}



resource "aws_ecr_repository" "mcp-ai-orchestrator-agent" {
  name = "${var.mcp-ai-orchestrator-agent}"
  image_tag_mutability = "MUTABLE"
  tags = var.tags
  image_scanning_configuration {
    scan_on_push = false
  }
}

