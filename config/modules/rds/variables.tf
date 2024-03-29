variable "allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = string
}

variable "instance_class" {
  description = "The instance type of the RDS instance"
  type        = string
}

variable "name" {
  description = "The DB name to create. If omitted, no database is created initially"
  type        = string
}

variable "username" {
  description = "Username for the master DB user"
  type        = string
  default     = "tracer"
}

variable "password" {
  description = "Password for the master DB user. Note that this may show up in logs, and it will be stored in the state file"
  type        = string
}

variable "port" {
  description = "The port on which the DB accepts connections"
  type        = string
}

variable "db_subnet_group_name" {
  description = "Name of DB subnet group. DB instance will be created in the VPC associated with the DB subnet group. If unspecified, will be created in the default VPC"
  type        = string
}

variable "parameter_group_name" {
  description = "Name of the DB parameter group to associate"
  type        = string
}

variable "availability_zone" {
  description = "The Availability Zone of the RDS instance"
  type        = string
  default     = ""
}

variable "max_allocated_storage" {
  description = "Specifies the value for Storage Autoscaling"
  type        = number
}

variable "maintenance_window" {
  description = "The window to perform maintenance in. Syntax: 'ddd:hh24:mi-ddd:hh24:mi'. Eg: 'Mon:00:00-Mon:03:00'"
  type        = string
}

variable "ecs_task_sg_id" {
  type        = string
  description = "security group id of worker node sg"
}

variable "vpc_id" {
  type        = string
  description = "underlying vpc id"
}
