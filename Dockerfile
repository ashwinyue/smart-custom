# Dockerfile for Smart Custom API

# 使用Python 3.11官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    API_PORT=8001

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装uv
RUN pip install uv

# 复制项目文件
COPY pyproject.toml ./
COPY .env.example ./.env

# 安装依赖
RUN uv sync --frozen

# 复制源代码
COPY src/ ./src/
COPY main.py ./

# 暴露端口
EXPOSE 8001

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# 启动应用
CMD ["uv", "run", "python", "main.py"]