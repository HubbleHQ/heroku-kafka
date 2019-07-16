export PROJECT_NAME := $(notdir $(CURDIR))
PYTHON_2_BUILD := hbl/heroku-kafka:python2.7
PYTHON_3_BUILD := hbl/heroku-kafka:python3.7

.PHONY: dev-build
dev-build:
	docker build ./ -f dockerfiles/python2.7/Dockerfile -t $(PYTHON_2_BUILD) \
	&& docker build ./ -f dockerfiles/python3.7/Dockerfile -t $(PYTHON_3_BUILD)

.PHONY: dev-test
dev-test:
	docker run  --env-file .env $(PYTHON_2_BUILD) python test.py
	docker run  --env-file .env $(PYTHON_3_BUILD) python test.py

