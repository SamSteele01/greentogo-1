LOCAL_USERNAME := $(shell whoami)
REVISION := $(shell git log -n 1 --pretty=format:"%H")
HOSTNAME := 'greentogo'

PIPTOOLS_INSTALLED := $(shell command -v pip-sync 2> /dev/null)
NPM_INSTALLED := $(shell command -v npm 2> /dev/null)
BOWER_INSTALLED := $(shell command -v bower 2> /dev/null)
NODESASS_INSTALLED := $(shell command -v node-sass 2> /dev/null)

.PHONY: deploy-staging deploy-production requirements server update-requirements check check-pip-tools check-bower check-npm check-node-sass

check: check-pip-tools check-bower
	@echo "You have all required programs installed."

check-pip-tools:
ifndef PIPTOOLS_INSTALLED
	@echo "Installing pip-tools"
	pip install pip-tools
endif

check-bower: check-npm
ifndef BOWER_INSTALLED
	@echo "Installing bower"
	npm install -g bower
endif

check-node-sass: check-npm
ifndef NODESASS_INSTALLED
	@echo "Installing node-sass"
	npm install -g node-sass
endif

check-npm:
ifndef NPM_INSTALLED
	$(error "npm is not installed. Please install npm before continuing.")
endif

server: requirements
	./greentogo/manage.py runserver_plus

requirements: requirements.txt dev-requirements.txt bower.json check-pip-tools check-bower
	pip-sync requirements.txt dev-requirements.txt
	bower install

requirements.txt: requirements.in
	pip-compile requirements.in

dev-requirements.txt: dev-requirements.in
	pip-compile dev-requirements.in

update-requirements: check-pip-tools
	pip-compile --upgrade requirements.in
	pip-compile --upgrade dev-requirements.in

deploy-staging:
	ansible-playbook -i deployment/environments/staging/hosts --vault-password-file=.password  deployment/playbook.yml
	curl https://api.rollbar.com/api/1/deploy/ \
		-F access_token=$(ROLLBAR_KEY) \
		-F environment=staging \
		-F revision=$(REVISION) \
		-F local_username=$(LOCAL_USERNAME)

deploy-production:
	ansible-playbook -i deployment/environments/production/hosts --vault-password-file=.password  deployment/playbook.yml
	curl https://api.rollbar.com/api/1/deploy/ \
		-F access_token=$(ROLLBAR_KEY) \
		-F environment=production \
		-F revision=$(REVISION) \
		-F local_username=$(LOCAL_USERNAME)

greentogo/greentogo/.env:
	cp greentogo/greentogo/.env.sample greentogo/greentogo/.env
	@echo
	@echo "You will need to add database and API information to"
	@echo "the greentogo/greentogo/.env file. See README.md for"
	@echo "more information."
	@echo
