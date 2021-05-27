.PHONY: check test deploy deploy-with-secrets-file

check: ## Run linters
		@echo "*** running linters ***"
		flake8 --count --show-source --statistics
		@echo "*** all linters passing ***"
test: check ## Run tests
		@echo "*** running tests ***"
		PYTHONPATH=./src pytest --cov=src --cov-branch --cov-report term-missing
		@echo "*** all tests passing ***"
deploy: test ## Deploy project when secrets are exported as env variables
		@echo "*** running deploy ***"
		terraform apply
deploy-with-secrets-file: test ## Deploy project when secrets are stored in secrets.tfvars file
		@echo "*** running deploy ***"
		terraform apply -var-file=secrets.tfvars