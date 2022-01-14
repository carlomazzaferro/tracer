variable "ecs_cluster_name" {
  default = "tracer"
}

variable "private_subnets" {
  type = "list"
}

variable "public_subnets" {
  type = "list"
}

variable "vpc_id" {}
