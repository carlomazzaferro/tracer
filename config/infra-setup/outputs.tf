output "service_repo" {
  value = module.ecr.service_repo_name
}

output "celery_repo" {
  value = module.ecr.celery_repo_name
}