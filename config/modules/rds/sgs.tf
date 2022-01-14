resource "aws_security_group" "rds" {
  name   = "tracer-postgres-db-sg"
  vpc_id = var.vpc_id
}

resource "aws_security_group_rule" "allow-ecs-to-rds" {
  description              = "Allow ecs tasks to communicate with database"
  from_port                = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = var.ecs_task_sg_id
  to_port                  = 5432
  type                     = "ingress"
}

