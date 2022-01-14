## Spec

Please refer to
the [Worktest Solution Proposal](https://elegant-journey-920.notion.site/Worktest-8e012b89dea641eeb713345d55bd8d2b) for
an overview of the implementation decisions, architecture overview, and future directions.

This README will go over just the code itself and its structure, as well as how to interact with/develop against it

## Code structure

```text
 ┌── README.md                       <- The top-level README 
 ├── .github/workflows/dev-full.yaml <- CICD pipeline definition
 │         
 │          
 │── config                          <- IaC configuration Terraform provisioning
 │       ├── infra-setup             <- Terraform common resources deployment
 │       ├── dev                     <- Terraform dev environemnt deployment 
 │       └── modules
 │          ├── container            <- Service definitions
 │          ├── ecs                  <- ECS cluster definition
 │          ├── redis                <- ElastiCache definition
 │          ├── rds                  <- PostgresDB definition
 │          ├── ecr                  <- ECR and IAM      
 │          └── networking           <- VPCs, Subnets, ALB, security groups
 │
 ├── service                         <- Services definition
 │        ├── app/tracer             <- Main application codebase. Services, APIs, etc. The main application
 │        │                             and the celery worker have indeed the same code, just different 
 │        │                             entrypoints/Docker images
 │        ├── app/tests              <- App tests 
 │        ├── app/alembic            <- Db migrations 
 │        └── ...                    <- Dockerfiles, scripts, reqs
 ├── docker-compose.*                <- docker-compose files for local dev, deployemnt and testing
 │                                 
 └── Makefile                        <- Good ol Makefile with all the goodies to deploy, test all the code, 
                                        as well as installing dependencies
```

## Locally running the services

Fill in the `.secrets.env` with your RPC URL, and then:

```shell
>>> ENV=local make up
```

Head to http://localhost:8080/docs to check out the live Swagger docs

### Logs from services

```shell
# Celery
>>> docker logs -f $(docker ps -qf "name=tracer_celeryworker" ) | tee >(grep -v "^{") | grep "^{" | jq .
# Service
>>> docker logs -f $(docker ps -qf "name=tracer_tracer" ) | tee >(grep -v "^{") | grep "^{" | jq .
```

## Deployment

Live service is running at: http://tf-lb-20220114101120157800000005-1077470328.eu-central-1.elb.amazonaws.com:8080/docs

The celery service is deployed as a separate ECS service, enabling transparent autoscaling of each of the components.

The services are backed by an RDS instance, use an ElastiCache single node instance as a message broker, and are
deployed inside a VPC with an ALB in front of it, ensuring that all traffic within the VPC is unreacheable from the
outside world.

### CICD & IaC configs

The entire stack is automatically deployed on push via
the [CICD pipeline](https://github.com/carlomazzaferro/tracer/actions). The pipeline is minimal, and some components are
stubs, but it achieves the goal of reaching a true CICD system.

The deployment is done in two steps:

1. Deploy ECR repositories and IAM roles
2. Build & Push images do those ECR repos
3. Run tests [not yet implemented]
4. Deploy to "dev" - deploys rest of the cloud stack

Terraform modules were used to make the code re-usable, extensible, and easy to follow. Further, the system can easily
be extended to include a deployment of staging as well as production environment by simple re-using the modules and
passing in the tailored configs for that environment (e.g. larger RDS, more worker nodes, etc.)

Secrets management currently is pretty crude: we just store the secrets in the GH repo secrets, and pass them to the
configs via terraform TF_VAR. A better solution could be using a proper secrets management tool
like [sops](https://github.com/mozilla/sops)








