output "source_bucket_name" {
  value = aws_s3_bucket.source_bucket.bucket
}


output "source_bucket_arn" {
  value = aws_s3_bucket.source_bucket.arn
}


output "vector_bucket_name" {
  value = "${var.environment}-${var.source_bucket}-vector"
}