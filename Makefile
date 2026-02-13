# ============================================
# ShieldBank: Financial Crime Detection
# ============================================

# Installation
install_requirements:
	@pip install -r requirements.txt

install:
	@pip install . -U

# Cleanup
clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr proj-*.dist-info
	@rm -fr proj.egg-info

# Testing
test_structure:
	@bash tests/test_structure.sh

# Run Applications
run_api:
	@uvicorn api.fastapi:app --reload --port 8000

run_streamlit:
	@streamlit run streamlit_app/app.py

# Docker - Local
docker_build_local:
	docker build --tag=$(DOCKER_IMAGE_NAME):local .

docker_run_local:
	docker run -e PORT=8000 -p $(DOCKER_LOCAL_PORT):8000 --env-file .env $(DOCKER_IMAGE_NAME):local

# Docker - Cloud
DOCKER_IMAGE_PATH := $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME)

docker_build:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE_PATH):prod .

docker_run:
	docker run --platform linux/amd64 -e PORT=8000 -p $(DOCKER_LOCAL_PORT):8000 --env-file .env $(DOCKER_IMAGE_PATH):prod

# GCP Deployment
gcloud_setup:
	gcloud config set project $(GCP_PROJECT)
	gcloud auth configure-docker $(GCP_REGION)-docker.pkg.dev

gcloud_create_repo:
	gcloud artifacts repositories create $(DOCKER_REPO_NAME) \
		--repository-format=docker \
		--location=$(GCP_REGION) \
		--description="ShieldBank Docker Repository"

gcloud_push:
	docker push $(DOCKER_IMAGE_PATH):prod

gcloud_deploy:
	gcloud run deploy \
		--image $(DOCKER_IMAGE_PATH):prod \
		--memory $(GAR_MEMORY) \
		--region $(GCP_REGION) \
		--env-vars-file .env.yaml
