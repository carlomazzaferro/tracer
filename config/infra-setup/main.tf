provider "aws" {
  region  = var.aws_region
  version = ">= 2.38.0"
}

terraform {
  backend "s3" {
    encrypt = "true"
    bucket  = "terraform-backend-statefile"
    key     = "tracer-deployment-infra"
  }
}

module "ecr" {
  source     = "../modules/ecr"
  repo_names = [
    var.service_repo_name,
    var.celery_repo_name
  ]
}

