output "service_repo_name" {
  value = aws_ecr_repository.service.repository_url
}

output "execution_role_arn" {
  value = aws_iam_role.ecr_admin_role.arn
}
