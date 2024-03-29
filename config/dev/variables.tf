variable "region" {
  default = "eu-central-1"
}

variable "ami" {
  type        = map(string)
  description = "AWS ECS AMI id"

  default = {
    us-east-1      = "ami-cb2305a1"
    us-west-1      = "ami-bdafdbdd"
    us-west-2      = "ami-ec75908c"
    eu-west-1      = "ami-13f84d60"
    eu-central-1   = "ami-c3253caf"
    ap-northeast-1 = "ami-e9724c87"
    ap-southeast-1 = "ami-5f31fd3c"
    ap-southeast-2 = "ami-83af8ae0"
  }
}

variable "cidr_block" {
  default = "172.17.0.0/16"
}

variable "az_count" {
  default = "2"
}

variable "server_image_url" {
  description = "backend server ecr image url"
}

variable "celery_image_url" {
  description = "celery ecr image url"
}
variable "environment" {
  description = "env we're deploying to"
  default     = "dev"
}

variable "postgres_password" {
  description = "postgres db pw"
}

variable "rpc_url" {
  description = "URL of the Ethereum RPC service"
}