resource "aws_ecr_repository" "service" {
  name = var.repo_names[0]
}

resource "aws_ecr_repository" "celery" {
  name = var.repo_names[1]
}


resource "aws_iam_role_policy" "ecr_admin_policy" {
  name = "ecr_admin_policy"
  role = aws_iam_role.ecr_admin_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ecr:*",
        "logs:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "ecr_admin_role" {
  name               = "erc_admin_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
