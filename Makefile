.PHONY: help install test lint format run clean docker-build docker-run

help:
	@echo "Elena - Automated Solana Trading Bot"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      Install dependencies"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linter"
	@echo "  make format       Format code with black"
	@echo "  make run          Run Elena"
	@echo "  make clean        Clean up generated files"
	@echo "  make docker-build Build Docker image"
	@echo "  make docker-run   Run with Docker Compose"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

test:
	pytest tests/ -v --cov=. --cov-report=html

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:
	black .

run:
	python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build

docker-build:
	docker build -t elena:latest .

docker-run:
	docker-compose up -d

docker-logs:
	docker-compose logs -f elena

docker-stop:
	docker-compose down
