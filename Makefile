.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

config: build format ## setups the suite to be executed

# TODO add --no-cache to prevent missing new package versions
build: ## Build the base image
	docker build . -t search_service

up: ## run the container
	docker run -t search_service

bash: ## Run the service and open the app terminal
	docker run -it -t search_service bash

format: ## run the project formatters and linters
	docker run -it -t search_service black . --line-length 82 && flake8 . && isort .
