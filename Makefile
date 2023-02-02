# =================================================================================================
# Settings
# =================================================================================================
PROJECT := review-bot
PROJECT_PATH := $(shell pwd)
PYTHON := python3.8
PIP := pip3

IMAGE_NAME := review-bot-image
CONTAINER_NAME := review-bot

VENV_NAME := venv
PYTHONPATH := ${PROJECT_PATH}:${PYTHONPATH}

RM := rm -rf

# =================================================================================================
# Development
# =================================================================================================
create_venv:
	virtualenv --python="${PYTHON}" ${VENV_NAME} && ${VENV_NAME}/bin/pip3 install -r requirements.txt

clean:
	find . -name '*.pyc' -exec $(RM) {} +
	find . -name '*.pyo' -exec $(RM) {} +
	find . -name '*~' -exec $(RM)  {} +
	find . -name '__pycache__' -exec $(RM) {} +
	$(RM) .cache/ .pytest_cache/ *.egg-info

isort:
	isort ${PROJECT_PATH}

black:
	black ${PROJECT_PATH}

flake8:
	flake8 ${PROJECT_PATH}

lint_all: isort black flake8

# =================================================================================================
# Migrations
# =================================================================================================
db_upgrade_all:
	alembic upgrade head

db_downgrade_all:
	alembic downgrade base

db_current:
	alembic current
# =================================================================================================
# Deployment
# =================================================================================================

docker_build:
	docker build -t ${IMAGE_NAME} .

docker_rmi:
	docker rmi ${IMAGE_NAME} || true

docker_clean: docker_stop docker_rmi

docker_run:
	docker run -it -d \
	-v $(shell pwd)/.env:/${PROJECT}/.env \
	-v $(shell pwd)/data:/${PROJECT}/data \
	-v $(shell pwd)/logs:/${PROJECT}/logs \
	-v $(shell pwd)/configs:/${PROJECT}/configs \
	--name ${CONTAINER_NAME} ${IMAGE_NAME}

docker_run_hm:
	docker run -it --net=host -d \
	-v $(shell pwd)/.env:/${PROJECT}/.env \
	-v $(shell pwd)/data:/${PROJECT}/data \
	-v $(shell pwd)/logs:/${PROJECT}/logs \
	-v $(shell pwd)/configs:/${PROJECT}/configs \
	--name ${CONTAINER_NAME} ${IMAGE_NAME}

docker_stop:
	docker stop ${CONTAINER_NAME} || true

docker_deploy: docker_stop docker_clean docker_build docker_run

docker_deploy_hm: docker_stop docker_clean docker_build docker_run_hm



