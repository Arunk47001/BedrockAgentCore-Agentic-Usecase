resource "aws_s3_bucket" "source_bucket" {
  bucket = "${var.environment}-${var.source_bucket}"
  tags = var.tags
  acl = "private"
}