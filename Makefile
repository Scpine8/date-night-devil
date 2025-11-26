.PHONY: help install start dev stop test lint format format-check clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

start: ## Start the FastAPI server
	uvicorn app.main:app --reload

dev: start ## Alias for start (development mode)

run: start ## Alias for start

stop: ## Stop the server (if running in background)
	@echo "Stop the server manually (Ctrl+C) or kill the process"

test: ## Run tests (placeholder for future test suite)
	@echo "Tests not yet implemented"

lint: ## Run Ruff linter
	ruff check .

format: ## Format code with Ruff
	ruff format .

format-check: ## Check if code is formatted correctly (CI-friendly)
	ruff format --check .

clean: ## Clean Python cache files
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true

setup: install ## Install dependencies and setup project
	@echo "Project setup complete!"

