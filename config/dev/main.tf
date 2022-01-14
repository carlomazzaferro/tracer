terraform {
  backend "s3" {
    bucket = "terraform-backend-statefile"
    key    = "tracer-deployment"
    region = "eu-central-1"
  }
}

provider "aws" {
  region  = var.region
  version = ">= 2.38.0"
}


# Fetch AZs in the current region
data "aws_availability_zones" "available" {}

data "aws_iam_role" "ecr_admin_role" {
  name = "erc_admin_role"
}

module "server" {
  source             = "../modules/container"
  ecs_cluster_sg     = module.network.ecs_task_sg
  allow_all_sg       = module.network.allow_all_sg
  execution_role_arn = data.aws_iam_role.ecr_admin_role.arn
  cluster_id         = module.ecs.ecs_cluster_id
  vpc_id             = module.network.vpc_id
  private_subnets    = module.network.private_subnets
  public_subnets     = module.network.public_subnets
  docker_image       = var.server_image_url
  container_family   = "server"
  health_check_path  = "/healthz"
  container_port     = 8080
  loadbalancer_port  = 80
  cpu                = 512
  memory             = 1024
  instance_count     = 1
  timeout            = 180
}

module "network" {
  source     = "../modules/networking"
  cidr_block = var.cidr_block
}

module "ecs" {
  source           = "../modules/ecs"
  ecs_cluster_name = "tracer-ecs"
  vpc_id           = module.network.vpc_id
  private_subnets  = module.network.private_subnets
  public_subnets   = module.network.public_subnets
}

module "ecr" {
  source     = "../modules/ecr"
  repo_names = []
}

module "redis" {
  source            = "../modules/redis"
  sg_id             = module.network.ecs_task_sg
  subnet_group_name = module.network.private_subnets
  vpc_id            = module.network.vpc_id
}