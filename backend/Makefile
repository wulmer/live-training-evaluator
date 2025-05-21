PERSON?=${USER}
RANDOM=$(shell echo ${PERSON} | md5sum | cut -c 1-8)
AZURE_RESOURCE_GROUP=${PERSON}-lte-backend-rg
AZURE_CONTAINER_NAME=${PERSON}-lte-backend-container
AZURE_LOCATION=WestEurope
AZURE_CONTAINER_REGISTRY=${PERSON}lteacr
AZURE_ACR_USERNAME=${PERSON}ltetoken
AZURE_ACR_TOKEN=#will-be-read-from-file-after-docker-push
AZURE_ACR_TOKEN_FILE=.secret-acr-token
IMAGE_NAME=lte-backend
IMAGE_TAG=latest
DEPLOYED_HOSTNAME_FILE=.deployed-hostname.txt
AZURE_SQL_SERVER_NAME=${PERSON}-lte-sql-server
AZURE_SQL_ADMIN_USER=${PERSON}lteadmin
AZURE_SQL_DB_NAME=${PERSON}-lte-sql-db
AZURE_SQL_ADMIN_PASSWORD_FILE=.sql-admin-password.txt

SHELL=bash

help:
	@echo "Makefile for managing the backend application"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help            Show this help message"
	@echo "  dev             Run the application in development mode"
	@echo "  devmssql        Run the application in development mode with Azure SQL Database"
	@echo "  format          Format the code using ruff"
	@echo "  docker-build    Build the Docker image"
	@echo "  docker-run      Build and run the Docker container"
	@echo "  docker-push     Build and push the Docker image to Azure Container Registry"
	@echo "  deploy          Deploy the application to Azure Container Instance"
	@echo "  logs            Show logs of the Azure Container Instance"
	@echo "  restart				 Restart the Azure Container Instance"
	@echo "  swagger-url     Show the Swagger and Redoc URLs"
	@echo "  delete          Delete the Azure Container Instance and Resource Group"
	@echo ""
	@echo "If you want to deploy the application, you need to run these two steps:"
	@echo "  1. make docker-push"
	@echo "  2. make deploy"
	@echo "After you are done: make delete"

dev:
	uv run uvicorn app.main:app --reload

devmssql:
	AZURE_SQL_CONNECTION_STRING="mssql+pyodbc://${AZURE_SQL_ADMIN_USER}:$$(<${AZURE_SQL_ADMIN_PASSWORD_FILE})@${AZURE_SQL_SERVER_NAME}.database.windows.net:1433/${AZURE_SQL_DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server" \
	uv run uvicorn app.main:app --reload

format:
	uv run ruff format .

docker-build:
	docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

docker-run: docker-build
	docker run \
		-p 8000:8000 \
		--env AZURE_SQL_CONNECTION_STRING="mssql+pyodbc://${AZURE_SQL_ADMIN_USER}:$$(<${AZURE_SQL_ADMIN_PASSWORD_FILE})@${AZURE_SQL_SERVER_NAME}.database.windows.net:1433/${AZURE_SQL_DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server" \
		${IMAGE_NAME}:${IMAGE_TAG}

docker-push: docker-build
	az group create \
		--name ${AZURE_RESOURCE_GROUP} \
		--location "${AZURE_LOCATION}"
	az acr create \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_REGISTRY} \
		--sku Basic
	if command -v podman &> /dev/null ; then \
		podman login \
			${AZURE_CONTAINER_REGISTRY}.azurecr.io \
			-u 00000000-0000-0000-0000-000000000000 \
			-p "$$(az acr login --name ${AZURE_CONTAINER_REGISTRY} --expose-token -o tsv --query accessToken)" ; \
	else \
		az acr login \
			--name ${AZURE_CONTAINER_REGISTRY} ; \
	fi
	az acr token create \
		--name ${AZURE_ACR_USERNAME} \
		--registry ${AZURE_CONTAINER_REGISTRY} \
		--expiration-in-days 30 \
		--repository ${IMAGE_NAME} "content/read" \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--output tsv \
		--query "credentials.passwords[0].value" > ${AZURE_ACR_TOKEN_FILE}
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${AZURE_CONTAINER_REGISTRY}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}
	docker push ${AZURE_CONTAINER_REGISTRY}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

deploy:
	openssl rand -base64 32 | tr -d '\n' > ${AZURE_SQL_ADMIN_PASSWORD_FILE}
	az group create \
		--name ${AZURE_RESOURCE_GROUP} \
		--location "${AZURE_LOCATION}"
	az sql server create \
		--name ${AZURE_SQL_SERVER_NAME} \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--location "${AZURE_LOCATION}" \
		--admin-user ${AZURE_SQL_ADMIN_USER} \
		--admin-password $$(<${AZURE_SQL_ADMIN_PASSWORD_FILE}) \
		--enable-public-network false \
		--minimal-tls-version 1.2
	az sql db create \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--server ${AZURE_SQL_SERVER_NAME} \
		--name ${AZURE_SQL_DB_NAME} \
		--backup-storage-redundancy Local \
		--tier GeneralPurpose \
		--family Gen5 \
		--capacity 2 \
		--compute-model Serverless \
		--use-free-limit \
		--free-limit-exhaustion-behavior AutoPause
	az sql server update \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_SQL_SERVER_NAME} \
		--set publicNetworkAccess="Enabled"
	az sql server firewall-rule create \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--server ${AZURE_SQL_SERVER_NAME} \
		--name AllowAllWindowsAzureIps \
		--start-ip-address 0.0.0.0 \
		--end-ip-address 0.0.0.0
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
		--registry-password $$(<${AZURE_ACR_TOKEN_FILE}) \
		--cpu 1 \
		--memory 1.5 \
		--ports 8000 \
		--ip-address public \
		--dns-name-label ${AZURE_CONTAINER_NAME}-${RANDOM} \
		--environment-variables \
			AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING} \
			AZURE_SQL_CONNECTION_STRING="mssql+pyodbc://${AZURE_SQL_ADMIN_USER}:$$(<${AZURE_SQL_ADMIN_PASSWORD_FILE})@${AZURE_SQL_SERVER_NAME}.database.windows.net:1433/${AZURE_SQL_DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server" \
		--restart-policy OnFailure \
		--output tsv \
		--query "ipAddress.fqdn" | tee ${DEPLOYED_HOSTNAME_FILE}

logs:
	az container logs \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME} \
		--follow

restart:
	az container restart \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME}

swagger-url:
	@echo "Swagger URL: http://$$(< ${DEPLOYED_HOSTNAME_FILE}):8000/docs"
	@echo "Redoc URL: http://$$(< ${DEPLOYED_HOSTNAME_FILE}):8000/redoc"	

delete:
	az container delete \
		--resource-group ${AZURE_RESOURCE_GROUP} \
		--name ${AZURE_CONTAINER_NAME} \
		--yes
	az group delete \
		--name ${AZURE_RESOURCE_GROUP} \
		--yes
	rm -f ${DEPLOYED_HOSTNAME_FILE}
	rm -f ${AZURE_ACR_TOKEN_FILE}
	rm -f ${AZURE_SQL_ADMIN_PASSWORD_FILE}
	@echo "Deleted Azure Container Instance and Resource Group"