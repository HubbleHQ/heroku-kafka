export PROJECT_NAME := $(notdir $(CURDIR))
PYTHON_3_BUILD := python3

.PHONY: dev-build
dev-build: ## Build the docker boxes required to test the build
	docker compose build

.PHONY: dev-test
dev-test: ## Run package tests in both Python 2 & 3
	docker compose run --rm $(PYTHON_3_BUILD) python test.py

package: ## Generate a dist package to send to pypi and check it is valid
	docker compose run --rm $(PYTHON_3_BUILD) python setup.py sdist bdist_wheel
	docker compose run $(PYTHON_3_BUILD) python -m twine check dist/*

.PHONY: upload-test
upload-test: ## Upload the dist package to pypi test server
	docker compose run $(PYTHON_3_BUILD) python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## Upload the dist package to pypi server
	docker compose run $(PYTHON_3_BUILD) python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: dev-shell
dev-shell: ## Creates a shell in the project container
	docker compose run --rm $(PROJECT_NAME) bash

.PHONY: help
help: ## This message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help