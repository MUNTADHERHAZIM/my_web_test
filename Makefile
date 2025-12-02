# Makefile for Muntazir Portfolio Project

.PHONY: help install dev test lint format clean build deploy docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  dev          - Run development server"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean temporary files"
	@echo "  migrate      - Run database migrations"
	@echo "  makemigrations - Create new migrations"
	@echo "  collectstatic - Collect static files"
	@echo "  createsuperuser - Create superuser"
	@echo "  shell        - Open Django shell"
	@echo "  dbshell      - Open database shell"
	@echo "  loaddata     - Load sample data"
	@echo "  dumpdata     - Dump database data"
	@echo "  build        - Build for production"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up    - Start Docker containers"
	@echo "  docker-down  - Stop Docker containers"
	@echo "  docker-logs  - View Docker logs"
	@echo "  docker-shell - Open shell in Docker container"
	@echo "  pre-commit   - Install pre-commit hooks"
	@echo "  security     - Run security checks"
	@echo "  deps-update  - Update dependencies"
	@echo "  backup       - Backup database"
	@echo "  restore      - Restore database"

# Development setup
install:
	pip install -r requirements/development.txt
	pre-commit install
	npm install

dev:
	python manage.py runserver 0.0.0.0:8000

# Testing
test:
	pytest

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-fast:
	pytest --maxfail=1 --disable-warnings -q

test-slow:
	pytest -m slow

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

# Code quality
lint:
	flake8 .
	mypy .
	bandit -r . -x tests/
	djlint --check templates/
	pylint **/*.py

format:
	black .
	isort .
	djlint --reformat templates/

format-check:
	black --check .
	isort --check-only .

# Database operations
migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

migrations-check:
	python manage.py makemigrations --check --dry-run

showmigrations:
	python manage.py showmigrations

# Static files
collectstatic:
	python manage.py collectstatic --noinput

compress:
	python manage.py compress

# User management
createsuperuser:
	python manage.py createsuperuser

# Django shell
shell:
	python manage.py shell

shell-plus:
	python manage.py shell_plus

dbshell:
	python manage.py dbshell

# Data management
loaddata:
	python manage.py loaddata fixtures/initial_data.json

load-sample-data:
	python manage.py load_sample_data

dumpdata:
	python manage.py dumpdata --indent=2 > backup_data.json

dumpdata-auth:
	python manage.py dumpdata auth.User --indent=2 > users_backup.json

dumpdata-blog:
	python manage.py dumpdata blog --indent=2 > blog_backup.json

dumpdata-core:
	python manage.py dumpdata core --indent=2 > core_backup.json

# Translation
makemessages:
	python manage.py makemessages -l ar
	python manage.py makemessages -l en

compilemessages:
	python manage.py compilemessages

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Build
build:
	npm run build
	python manage.py collectstatic --noinput
	python manage.py compress

# Docker operations
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-restart:
	docker-compose restart

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec web bash

docker-db-shell:
	docker-compose exec db psql -U postgres -d muntazir_portfolio

docker-redis-shell:
	docker-compose exec redis redis-cli

docker-clean:
	docker system prune -f
	docker volume prune -f

# Pre-commit
pre-commit:
	pre-commit install
	pre-commit run --all-files

pre-commit-update:
	pre-commit autoupdate

# Security
security:
	bandit -r . -x tests/
	safety check
	pip-audit

# Dependencies
deps-check:
	pip-check
	pipdeptree

deps-update:
	pip-review --local --interactive

deps-outdated:
	pip list --outdated

# Performance
profile:
	python manage.py runprofileserver

benchmark:
	pytest --benchmark-only

# Backup and restore
backup:
	python manage.py dbbackup
	python manage.py mediabackup

restore:
	python manage.py dbrestore
	python manage.py mediarestore

# Health checks
check:
	python manage.py check
	python manage.py check --deploy

health:
	./docker/healthcheck.sh

# Monitoring
stats:
	python manage.py show_urls
	python manage.py graph_models -a -g -o models.png

# Deployment
deploy-staging:
	@echo "Deploying to staging..."
	git push staging main

deploy-production:
	@echo "Deploying to production..."
	git push production main

# Local development helpers
reset-db:
	rm -f db.sqlite3
	python manage.py migrate
	python manage.py load_sample_data

fresh-install:
	make clean
	make install
	make migrate
	make load-sample-data
	make collectstatic

# Documentation
docs:
	sphinx-build -b html docs/ docs/_build/html/

docs-serve:
	cd docs/_build/html && python -m http.server 8080

# Internationalization
i18n:
	make makemessages
	make compilemessages

# Full setup for new developers
setup:
	@echo "Setting up development environment..."
	make install
	make migrate
	make load-sample-data
	make collectstatic
	make pre-commit
	@echo "Setup complete! Run 'make dev' to start the development server."

# CI/CD helpers
ci-test:
	pytest --cov=. --cov-report=xml --junitxml=test-results.xml

ci-lint:
	flake8 . --format=junit-xml --output-file=flake8-results.xml
	black --check .
	isort --check-only .

ci-security:
	bandit -r . -x tests/ -f json -o bandit-results.json

safety-check:
	safety check --json --output safety-results.json

# Environment management
env-create:
	python -m venv venv

env-activate:
	@echo "Run: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)"

env-deactivate:
	deactivate

# Quick commands
qs: # Quick start
	make migrate
	make dev

qt: # Quick test
	make test-fast

qf: # Quick format
	make format

ql: # Quick lint
	flake8 . --select=E9,F63,F7,F82

# Help for specific areas
help-docker:
	@echo "Docker commands:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-up     - Start containers"
	@echo "  docker-down   - Stop containers"
	@echo "  docker-logs   - View logs"
	@echo "  docker-shell  - Open container shell"

help-test:
	@echo "Testing commands:"
	@echo "  test          - Run all tests"
	@echo "  test-cov      - Run tests with coverage"
	@echo "  test-fast     - Run tests quickly"
	@echo "  test-unit     - Run unit tests only"
	@echo "  test-integration - Run integration tests only"

help-quality:
	@echo "Code quality commands:"
	@echo "  lint          - Run all linters"
	@echo "  format        - Format all code"
	@echo "  security      - Run security checks"
	@echo "  pre-commit    - Install and run pre-commit hooks"