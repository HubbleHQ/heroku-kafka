export PROJECT_NAME := $(notdir $(CURDIR))
PYTHON_2_BUILD := python2
PYTHON_3_BUILD := python3

.PHONY: dev-build
dev-build: ## Build the docker boxes required to test the build
	docker-compose build

.PHONY: dev-test
dev-test: ## Run package tests in both Python 2 & 3
	docker-compose run --rm $(PYTHON_2_BUILD) python test.py
	docker-compose run --rm $(PYTHON_3_BUILD) python test.py

package: ## Generate a dist package to send to pypi and check it is valid
	docker-compose run --rm $(PYTHON_3_BUILD) python setup.py sdist bdist_wheel
	docker-compose run $(PYTHON_3_BUILD) python -m twine check dist/*

.PHONY: upload-test
upload-test: ## Upload the dist package to pypi test server
	docker-compose run $(PYTHON_3_BUILD) python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## Upload the dist package to pypi server
	docker-compose run $(PYTHON_3_BUILD) python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

