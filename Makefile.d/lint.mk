
.PHONY: lint
lint: \
    lint-isort \
    lint-mypy \
    lint-flake8


.PHONY: lint-mypy
lint-mypy:
	$(TOOL)/mypy --config-file config/mypy.ini -p git_sage
	$(TOOL)/mypy --config-file config/mypy.ini -p git_sage_test


.PHONY: lint-flake8
lint-flake8:
	$(TOOL)/flake8 --statistics --config config/flake8-test git_sage git_sage_test


.PHONY: lint-isort
lint-isort:
	$(TOOL)/isort --settings config/isort.cfg git_sage git_sage_test


