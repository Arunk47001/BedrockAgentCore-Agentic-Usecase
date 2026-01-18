resource "null_resource" "run_script" {
  provisioner "local-exec" {
    command = "bash ${path.module}/s3_vector.sh ${var.environment} ${var.source_bucket}"
  }
   triggers = {
    always_run = timestamp()
  }
}