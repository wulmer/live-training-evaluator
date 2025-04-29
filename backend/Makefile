AZURE_RESOURCE_GROUP=ulw2si-lte-backend-rg
AZURE_CONTAINER_NAME=ulw2si-lte-backend-container
AZURE_LOCATION=WestEurope
AZURE_CONTAINER_REGISTRY=ulw2silteacr
IMAGE_NAME=lte-backend
IMAGE_TAG=latest

SHELL=bash

dev:
	uv run uvicorn app.main:app --reload

format:
	uv run ruff format .

docker-build:
	docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

docker-run: docker-build
	docker run -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}

docker-push: docker-build
	az group create \
		--name ${AZURE_RESOURCE_GROUP} \
		--location "${AZURE_LOCATION}"
	az acr create \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_REGISTRY} \
		--sku Basic
	az acr login \
		--name ${AZURE_CONTAINER_REGISTRY}
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${AZURE_CONTAINER_REGISTRY}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}
	docker push ${AZURE_CONTAINER_REGISTRY}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

logs:
	az container logs \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME} \
		--follow

deploy:
	az group create \
		--name ${AZURE_RESOURCE_GROUP} \
		--location "${AZURE_LOCATION}"
	az container create \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME} \
		--os-type Linux \
		--image ${AZURE_CONTAINER_REGISTRY}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} \
		--registry-login-server ${AZURE_CONTAINER_REGISTRY}.azurecr.io \
		--registry-username ${AZURE_ACR_USERNAME} \
		--registry-password ${AZURE_ACR_TOKEN} \
		--cpu 1 \
		--memory 1.5 \
		--ports 8000 \
		--ip-address public \
		--dns-name-label ${AZURE_CONTAINER_NAME}-$${RANDOM} \
		--environment-variables AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING} \
		--restart-policy OnFailure \
		--query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}"


delete:
	az container delete \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME} \
		--yes
	az group delete \
		--name ${AZURE_RESOURCE_GROUP} \
		--yes