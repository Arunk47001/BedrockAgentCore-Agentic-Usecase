terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.24.0"
    }
    null = {
      source = "hashicorp/null"
      version = "3.2.1"
    }
    template = {
      source = "hashicorp/template"
      version = "2.2.0"
    }
  }
}

provider aws{
    region = var.region
  }
