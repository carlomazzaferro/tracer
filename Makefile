.PHONY: help install clean local-service docker-build-celery docker-build-service docker-push-service docker-push-celery test-service

.DEFAULT_GOAL := help
SHELL := /bin/bash
PATH := ${PWD}/venv/bin:${PATH}
PYTHONPATH := ${PWD}:${PYTHONPATH}
AWS_DEFAULT_REGION = eu-central-1

include .common.env

ifdef ENV
include .${ENV}.env
endif

export


BOLD=$(shell tput -T xterm bold)
RED=$(shell tput -T xterm setaf 1)
GREEN=$(shell tput -T xterm setaf 2)
YELLOW=$(shell tput -T xterm setaf 3)
RESET=$(shell tput -T xterm sgr0)

help:
	@awk 'BEGIN {FS = ":.*?##-.*?local.*?- "} /^[a-zA-Z_-]+:.*?##-.*?local.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "${YELLOW}ENV=data${RESET}"
	@awk 'BEGIN {FS = ":.*?##-.*?data.*?- "} /^[a-zA-Z_-]+:.*?##-.*?data.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "${YELLOW}ENV=sandbox${RESET}"
	@awk 'BEGIN {FS = ":.*?##-.*?sandbox.*?- "} /^[a-zA-Z_-]+:.*?##-.*?sandbox.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


check-%:
	@if [ "${${*}}" = "" ]; then \
		echo -e "${RED} Variable $* not set ❌${RESET}"; \
		exit 1; \
	fi

nosudo:
	@if [ $(shell whoami) = root ]; then \
		echo -e "${RED} This command should not be run as root ❌${RESET}"; \
		exit 1; \
	fi

install: ##-local- Setup project
install: nosudo clean
	virtualenv -p python3.7 venv
	pip install -r dev-requirements.txt


clean: ##-local- Cleanup project
	rm -rf venv


# -------------------------------------------------------------------
# DOCKER
# -------------------------------------------------------------------


up:  ##-local- Build image
	docker-compose -f docker-compose.local.build.yml up --build

down:  ##-local- Build image
	docker-compose -f docker-compose.local.build.yml down


docker-build-service:  ##-local- Build image
	docker build -t ${DOCKER_REGISTRY}/${PROJECT_NAME}:${GITHUB_SHA} ./service


docker-build-celery:  ##-local- Build image
	docker build -f ./service/Dockerfile.celery -t ${DOCKER_REGISTRY}/${PROJECT_NAME}-celery:${GITHUB_SHA} ./service


docker-push-service:  ##-local- Build & push image to ECR
docker-push-service: docker-build-service
	aws ecr get-login-password | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}
	docker push ${DOCKER_REGISTRY}/${PROJECT_NAME}:${GITHUB_SHA}

docker-push-celery:  ##-local- Build & push image to ECR
docker-push-celery: docker-build-celery
	aws ecr get-login-password | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}
	docker push ${DOCKER_REGISTRY}/${PROJECT_NAME}-celery:${GITHUB_SHA}

# -------------------------------------------------------------------
# TEST
# -------------------------------------------------------------------


test-service:
	cp -R services/training services/backend/app
	docker build -f ./service/Dockerfile.test --build-arg ENV=test -t ${PROJECT_NAME}-base-test:latest ./service
	docker run -it ${PROJECT_NAME}-base-test:latest
	rm -rf services/backend/app/training


# -------------------------------------------------------------------
# DEPLOY
# -------------------------------------------------------------------

infra: check-ENV
	export TF_VAR_service_repo_name=${PROJECT_NAME} && \
	export TF_VAR_celery_repo_name=${PROJECT_NAME}-celery && \
	export TF_VAR_aws_region=${AWS_DEFAULT_REGION} && \
	cd config/infra-setup && \
	terraform init && \
	terraform apply -auto-approve


deploy: check-ENV
	export TF_VAR_server_image_url=${DOCKER_REGISTRY}/${PROJECT_NAME}:${GITHUB_SHA} && \
	export TF_VAR_celery_image_url=${DOCKER_REGISTRY}/${PROJECT_NAME}-celery:${GITHUB_SHA} && \
	export TF_VAR_postgres_password=${POSTGRES_PASSWORD} && \
	export TF_VAR_rpc_url=${RPC_URL} && \
	cd config/${ENV} && \
	terraform init && \
	terraform apply -auto-approve



# -------------------------------------------------------------------
# DEPLOY
# -------------------------------------------------------------------


destroy: check-ENV
	export TF_VAR_server_image_url=${DOCKER_REGISTRY}/${PROJECT_NAME}:latest && \
	cd config && \
	terraform init && \
	terraform destroy


