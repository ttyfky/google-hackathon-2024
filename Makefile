BIN := $(CURDIR)/.bin
PATH := $(abspath $(BIN)):$(PATH)

UNAME_OS := $(shell uname -s)
UNAME_ARCH := $(shell uname -m)

APP_NAME := b-moz

# This activate env vars.
include ./resources/secrets/.env


.PHONY: help
help: ## print help
	@grep -E '^[/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

$(BIN):
	mkdir -p $(BIN)

.PHONY: clean
clean: ## delete .bin directory
	rm -rf "$(BIN)"

.PHONY: os
os:
	@echo "$(UNAME_OS)"

CLOUD_SQL_PROXY := $(BIN)/cloud_sql_proxy
$(CLOUD_SQL_PROXY): | $(BIN)
	@curl -o $(CLOUD_SQL_PROXY) "https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64"
	@chmod +x $(CLOUD_SQL_PROXY)

.PHONY: sql_proxy
sql_proxy: | $(CLOUD_SQL_PROXY) ## bring up sql proxy with given config. use preset conns by default.
	$(CLOUD_SQL_PROXY)  -instances=${GCP_SQL_CONNS} -token=`gcloud auth print-access-token`

.PHONY: init
init:

.PHONY: setup
setup: $(BIN) ## setup
	@poetry config virtualenvs.in-project true
	@poetry install

.PHONY: lint
lint:
	@poetry run flake8 .

.PHONY: format
format:
	@poetry run black .

.PHONY: format-check
format-check:
	@poetry run black --diff .

.PHONY: pytest
pytest:
	@poetry run pytest


.PHONY: type-check
type-check:
	pyright

.PHONY: local-check
local-check: format lint type-check ## Check health of the project by running format, lint, and type-check but without test.

.PHONY: docker/build
docker/build:
	docker build . -t $(APP_NAME) --platform linux/amd64

GAR_PATH := asia-northeast1-docker.pkg.dev/$(PROJECT_NAME)/google-hackathon/$(APP_NAME):latest

.PHONY: gar/push

gar/push: docker/build
	docker tag $(APP_NAME)  $(GAR_PATH)
	docker push $(GAR_PATH)

.PHONY: deploy
deploy: gar/push
	gcloud --project=$(PROJECT_NAME) run deploy $(APP_NAME) --image $(GAR_PATH) --region asia-northeast1 --platform managed \
	  --service-account $(APP_NAME)-crun@$(PROJECT_NAME).iam.gserviceaccount.com
