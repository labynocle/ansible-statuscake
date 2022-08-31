.DEFAULT_GOAL := help

SHELL = /bin/bash
DEPLOY_REQ_FILE = requirements.txt
DEPLOY_REQ_SHA1 = $(shell sha1sum $(DEPLOY_REQ_FILE) | cut -f1 -d " " | sed -e 's/^\(.\{5\}\).*/\1/')
VENV_NAME = .venv-$(DEPLOY_REQ_SHA1)
PYTHON_BIN = $(VENV_NAME)/bin/python3
TEMPLATES_DIR = payloads_templates
PAYLOAD_DIR = payloads
LIBRARY_DIR = library
STATUSCAKE_TEST = uptime
STATUSCAKE_ACTION = create
STATUSCAKE_TEST_FULL_PATH = $(LIBRARY_DIR)/status_cake_$(STATUSCAKE_TEST).py
STATUSCAKE_ACTION_FULL_PATH = $(PAYLOAD_DIR)/args_$(STATUSCAKE_ACTION).json

# ##############################################################################
# Makefile targets/goals
# ##############################################################################
##
## Help commands
## -----
##

.PHONY: list
list: ## Generate basic list of all targets
	@grep '^[^\.#[:space:]].*:' Makefile | \
	        grep -v "=" | \
	        cut -d':' -f1

.PHONY: help
help: ## Makefile help
	@grep -E '(^[a-zA-Z_0-9%-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | \
	        awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | \
	        sed -e 's/\[32m##/[33m/'

##
## Env management commands
## -----
##

.PHONY: clean
clean: ## Clean virtal env
	@rm -rf $(VENV_NAME)
	@rm -rf $(PAYLOAD_DIR)

.PHONY: set-env
set-env: ## Generate virtual env and vault file
	@if [ ! -d "$(VENV_NAME)" ]; then \
	        python3 -m venv $(VENV_NAME) && \
	        $(PYTHON_BIN) -m pip install --upgrade pip setuptools && \
	        $(PYTHON_BIN) -m pip install -r $(DEPLOY_REQ_FILE) ; \
	fi

.PHONY: guard-%
guard-%: ## Check if a given env var is well set, usage: make guard-TRIGGER_TOKEN
	@if [ "${${*}}" = "" ]; then \
	       echo -e "\e[1m\e[31mProblem :: $* should be exported in your env\e[0m"; \
	       exit 1; \
	fi

.PHONY: generate-payloads
generate-payloads: guard-STATUSCAKE_API_KEY ## Generate payloads config
	@if [ ! -d "$(PAYLOAD_DIR)" ]; then mkdir $(PAYLOAD_DIR); fi
	@for a in $(TEMPLATES_DIR)/*;do sed -e "s/__STATUSCAKE_API_KEY__/$(STATUSCAKE_API_KEY)/g" $$a > $(PAYLOAD_DIR)/`basename $$a`;done

.PHONY: list-actions
list-actions: generate-payloads ## List all available actions values for STATUSCAKE_ACTION
	@ls -1 $(PAYLOAD_DIR)/ | sed -e "s/^args_\(.*\).json/\1/"

.PHONY: list-tests
list-tests: ## List all available tests values for STATUSCAKE_TEST
	@ls -1 $(LIBRARY)/ | sed -e "s/^status_cake_\(.*\).py$/\1/"

##
## Test commands
## -----
##

.PHONY: test
test: set-env ## Launch test by default STATUSCAKE_TEST=uptime and STATUSCAKE_ACTION=create
ifeq ("$(wildcard $(STATUSCAKE_TEST_FULL_PATH))","")
	@echo "$(STATUSCAKE_TEST_FULL_PATH) does not exist - please specify STATUSCAKE_TEST, eg make test STATUSCAKE_TEST=uptime"
	@echo "Possible values could be listed by make list-tests"
	@exit 1
endif
ifeq ("$(wildcard $(STATUSCAKE_ACTION_FULL_PATH))","")
	@echo "$(STATUSCAKE_ACTION_FULL_PATH) does not exist - please specify STATUSCAKE_ACTION, eg: make test STATUSCAKE_ACTION=create"
	@echo "Possible values could be listed by: make list-actions"
	@exit 1
endif
	@$(PYTHON_BIN) \
		$(STATUSCAKE_TEST_FULL_PATH) \
		$(STATUSCAKE_ACTION_FULL_PATH)
