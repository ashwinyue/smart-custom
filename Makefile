# Makefile for Smart Custom API

.PHONY: help install dev-install test lint format clean run dev

# Default target
help:
	@echo "Smart Custom API - 可用命令:"
	@echo ""
	@echo "  install      - 安装项目依赖"
	@echo "  dev-install  - 安装开发依赖"
	@echo "  test         - 运行测试"
	@echo "  lint         - 代码检查"
	@echo "  format       - 代码格式化"
	@echo "  clean        - 清理临时文件"
	@echo "  run          - 运行应用"
	@echo "  dev          - 开发模式运行应用"

# Install dependencies
install:
	uv sync

# Install development dependencies
dev-install:
	uv sync --dev

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

# Code linting
lint:
	uv run ruff check src/
	uv run mypy src/

# Code formatting
format:
	uv run ruff format src/
	uv run black src/

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Run the application
run:
	uv run python main.py

# Run the application in development mode
dev:
	uv run python main.py --reload