# =============================================================================
# Project: Automation & Integration Performance Analytics
# Stack: MySQL + Power BI (+ Python ETL helpers)
# Usage: run `make help` for available targets.
# =============================================================================

SHELL := /bin/bash

# ------- Configuration -------
PYTHON        ?= python3
PIP           ?= $(PYTHON) -m pip
VENV_DIR      ?= .venv
VENVPY        := $(VENV_DIR)/bin/python
VENVPIP       := $(VENV_DIR)/bin/pip
ENV_FILE      ?= .env
MAKEVARS_DIR  ?= .makevars
MAKEVARS_FILE ?= $(MAKEVARS_DIR)/exported.env

DB_HOST ?= localhost
DB_PORT ?= 3306
DB_USER ?= analytics
DB_PASSWORD ?= change_me
DB_NAME ?= automation_perf

MYSQL_DOCKER_NAME ?= analytics-mysql
MYSQL_ROOT_PASSWORD ?= root
MYSQL_IMAGE ?= mysql:8.0

# ------- Helpers -------
.DEFAULT_GOAL := help
.PHONY: help

$(MAKEVARS_DIR):
	@mkdir -p $(MAKEVARS_DIR)

# Export selected ENV to a file so subshell invocations share settings.
$(MAKEVARS_FILE): | $(MAKEVARS_DIR)
	@echo "DB_HOST=$(DB_HOST)" >  $(MAKEVARS_FILE)
	@echo "DB_PORT=$(DB_PORT)" >> $(MAKEVARS_FILE)
	@echo "DB_USER=$(DB_USER)" >> $(MAKEVARS_FILE)
	@echo "DB_PASSWORD=$(DB_PASSWORD)" >> $(MAKEVARS_FILE)
	@echo "DB_NAME=$(DB_NAME)" >> $(MAKEVARS_FILE)

env.export: $(MAKEVARS_FILE) ## Write effective DB_* env vars to .makevars/exported.env
	@echo "Wrote $(MAKEVARS_FILE)"

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\n\033[1mAvailable targets\033[0m:\n"} \
	/^[a-zA-Z0-9_%.\/-]+:.*?##/ { printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0,5) }' $(MAKEFILE_LIST)
	@echo ""

# ------- Environment -------
setup: ## Create virtualenv and install dev dependencies
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	@$(VENVPIP) install --upgrade pip
	@$(VENVPIP) install -r requirements-dev.txt || true
	@echo "Virtualenv ready at $(VENV_DIR)"

format: ## Run code formatters (black + isort)
	@$(VENVPY) -m black .
	@$(VENVPY) -m isort .

lint: ## Run linters (flake8 + mypy)
	@$(VENVPY) -m flake8 .
	@$(VENVPY) -m mypy . || true

test: ## Run test suite (pytest)
	@$(VENVPY) -m pytest -q

# ------- Database (MySQL) -------
db.up: ## Start MySQL in Docker (data stored in ./docker/mysql)
	@mkdir -p docker/mysql
	@docker rm -f $(MYSQL_DOCKER_NAME) >/dev/null 2>&1 || true
	@docker run -d --name $(MYSQL_DOCKER_NAME) \
		-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
		-e MYSQL_DATABASE=$(DB_NAME) \
		-e MYSQL_USER=$(DB_USER) \
		-e MYSQL_PASSWORD=$(DB_PASSWORD) \
		-p $(DB_PORT):3306 \
		-v $$PWD/docker/mysql:/var/lib/mysql \
		$(MYSQL_IMAGE)
	@echo "MySQL running at localhost:$(DB_PORT) (container: $(MYSQL_DOCKER_NAME))"

db.down: ## Stop and remove the MySQL container
	@docker rm -f $(MYSQL_DOCKER_NAME) >/dev/null 2>&1 || true
	@echo "MySQL container removed"

db.shell: ## Open a MySQL shell using env vars
	@docker exec -it $(MYSQL_DOCKER_NAME) \
		mysql -u$(DB_USER) -p$(DB_PASSWORD) -D $(DB_NAME)

db.migrate: ## Apply SQL migrations in ./migrations (ordered by filename)
	@test -d migrations || { echo "No migrations/ directory found"; exit 1; }
	@for f in $$(ls migrations/*.sql | sort); do \
		echo "Applying $$f"; \
		docker exec -i $(MYSQL_DOCKER_NAME) mysql -u$(DB_USER) -p$(DB_PASSWORD) -D $(DB_NAME) < $$f || exit 1; \
	done
	@echo "Migrations applied."

db.seed: ## Seed minimal demo data from ./seeds/*.sql
	@test -d seeds || { echo "No seeds/ directory found"; exit 1; }
	@for f in $$(ls seeds/*.sql | sort); do \
		echo "Seeding $$f"; \
		docker exec -i $(MYSQL_DOCKER_NAME) mysql -u$(DB_USER) -p$(DB_PASSWORD) -D $(DB_NAME) < $$f || exit 1; \
	done
	@echo "Seed data loaded."

db.dump: ## Dump database to ./artifacts/db_dump.sql
	@mkdir -p artifacts
	@docker exec $(MYSQL_DOCKER_NAME) \
		mysqldump -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) > artifacts/db_dump.sql
	@echo "Dump saved at artifacts/db_dump.sql"

# ------- ETL / Data Tasks (stubs) -------
run.extract: ## Run extraction step (stub: replace with your command)
	@echo ">> Implement extractor (e.g., $(VENVPY) -m etl.extract)"

run.load: ## Run load step (stub)
	@echo ">> Implement loader (e.g., $(VENVPY) -m etl.load)"

run.transform: ## Run transform step (stub)
	@echo ">> Implement transformer (e.g., $(VENVPY) -m etl.transform)"

run.quality: ## Run data quality checks (stub)
	@echo ">> Implement DQ checks (e.g., $(VENVPY) -m etl.checks)"

# ------- Power BI Integration -------
pbi.docs: ## Print guidance for Power BI workflow
	@echo "Power BI guidance:"
	@echo " - Build your model against mart_* views."
	@echo " - Prefer PBIT templates or PBIP projects for source control."
	@echo " - Document DAX measures and refresh strategy in /docs."
	@echo " - Use a gateway for on-prem MySQL, configure credentials securely."

# ------- Utilities -------
clean: ## Remove caches and temporary files
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@rm -rf .pytest_cache .mypy_cache .cache
	@echo "Cleaned."

distclean: clean ## Remove venv and artifacts
	@rm -rf $(VENV_DIR) artifacts/ docker/mysql/ $(MAKEVARS_DIR)
	@echo "Dist-cleaned."