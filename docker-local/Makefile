SHELL := /bin/bash -e

PROJECT_NAME = yumreport
.PHONY: *

export PROJECT_NAME

help: ## This help message
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

deploy:
	cd yumreport; docker stack deploy --compose-file ../docker-stack.yml $$PROJECT_NAME

tear-down:
	docker service rm $(PROJECT_NAME)_web
