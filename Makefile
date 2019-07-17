export PROJECT_NAME := $(notdir $(CURDIR))
PYTHON_2_BUILD := python2
PYTHON_3_BUILD := python3

.PHONY: dev-build
dev-build:
	docker-compose build

.PHONY: dev-test
dev-test:
	docker-compose run --rm $(PYTHON_2_BUILD) python test.py
	docker-compose run --rm $(PYTHON_3_BUILD) python test.py

package:
	docker-compose run --rm $(PYTHON_3_BUILD) python setup.py sdist bdist_wheel

.PHONY: upload
upload:
	docker-compose run $(PYTHON_3_BUILD) python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*


