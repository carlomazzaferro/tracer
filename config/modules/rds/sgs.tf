resource "aws_security_group" "rds" {
  name        = "${var.identifier}-sg"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "allow-nodes-to-rds" {
  description              = "Allow worker nodes to communicate with database"
  from_port                = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = var.node_sg_id
  to_port                  = 5432
  type                     = "ingress"
}

