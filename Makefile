.PHONY: help install clean local-service docker-build docker-push test-service

.DEFAULT_GOAL := help
SHELL := /bin/bash
PATH := ${PWD}/venv/bin:${PATH}
PYTHONPATH := ${PWD}:${PYTHONPATH}
AWS_DEFAULT_REGION = eu-central-1

DOCKER_REGISTRY = quantco

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


docker-build-tracer:  ##-local- Build image
	cp -R services/training services/backend/app
	docker build --build-arg ENV=prod -t ${DOCKER_REGISTRY}/${PROJ_NAME}:latest ./service
	rm -rf services/backend/app/training

docker-build-tracer:  ##-local- Build image
	cp -R services/training services/backend/app
	docker build --build-arg ENV=prod -t ${DOCKER_REGISTRY}/${PROJ_NAME}:latest ./service
	rm -rf services/backend/app/training



docker-push:  ##-local- Build & push image to ECR
docker-push: docker-build
	aws ecr get-login --region ${AWS_DEFAULT_REGION} --no-include-email | sh
	docker push ${DOCKER_REGISTRY}/${PROJ_NAME}


local-service:  ##-local- run everything locally
local-up: export ARGS=$(shell if [ "${logs}" != "true" ]; then echo "-d"; fi)
local-up: docker-build
	docker-compose -f docker-compose.yml up

local-down:
	docker-compose -f docker-compose.local.yml down


# -------------------------------------------------------------------
# TEST
# -------------------------------------------------------------------


test-service:
	cp -R services/training services/backend/app
	docker build -f ./services/backend/Dockerfile.test --build-arg ENV=test -t ${PROJ_NAME}-base-test:latest ./service
	docker run -it ${PROJ_NAME}-base-test:latest
	rm -rf services/backend/app/training


# -------------------------------------------------------------------
# DEPLOY
# -------------------------------------------------------------------


deploy: check-ENV
	export TF_VAR_server_image_url=${DOCKER_REGISTRY}/${PROJ_NAME}:latest && \
	cd config && \
	terraform init && \
	terraform apply -auto-approve



# -------------------------------------------------------------------
# DEPLOY
# -------------------------------------------------------------------


destroy: check-ENV
	export TF_VAR_server_image_url=${DOCKER_REGISTRY}/${PROJ_NAME}:latest && \
	cd config && \
	terraform init && \
	terraform destroy


