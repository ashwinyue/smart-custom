# Smart Custom API

基于FastAPI、LangChain和LangGraph的智能对话API，提供智能客服、订单查询、退款申请和热更新等功能。

## 功能特性

- 🤖 智能对话：基于OpenAI GPT-3.5-turbo模型的智能对话系统
- 📦 订单查询：支持订单状态查询和详细信息获取
- 💰 退款申请：自动化退款申请流程处理
- 🧾 发票生成：为指定订单生成电子发票
- 🔥 热更新功能：支持不重启服务的情况下更新模型和插件
- 📊 实时监控：提供API调用统计和性能监控
- 🔒 安全可靠：完善的错误处理和安全机制

## 技术栈

- **后端框架**：FastAPI
- **AI模型**：OpenAI GPT-3.5-turbo
- **AI框架**：LangChain + LangGraph
- **数据验证**：Pydantic
- **API文档**：自动生成的OpenAPI/Swagger文档
- **开发工具**：pytest, black, ruff, mypy

## 项目结构

```
smart-custom/
├── src/                    # 源代码目录
│   ├── api/               # API路由
│   │   └── chat_routes.py  # 对话相关路由
│   ├── core/              # 核心配置
│   │   └── config.py      # 应用配置
│   ├── models/            # 数据模型
│   │   └── chat_models.py # 对话模型
│   ├── services/          # 业务逻辑
│   │   ├── chat_service.py # 对话服务
│   │   ├── model_manager.py # 模型管理器
│   │   └── plugin_manager.py # 插件管理器
│   ├── tools/             # 工具函数
│   │   ├── invoice_tool.py  # 发票工具
│   │   ├── order_query.py   # 订单查询工具
│   │   └── refund_request.py # 退款申请工具
│   └── utils/             # 工具类
│       └── logger.py       # 日志工具
├── tests/                 # 测试目录
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   ├── test_hot_update.py # 热更新测试
│   └── test_invoice_plugin.py # 发票插件测试
├── docs/                  # 文档目录
│   ├── guide.md           # 使用指南
│   ├── homework_guide.md  # 作业指南
│   └── report.md          # 实验报告
├── .env                   # 环境变量
├── .gitignore            # Git忽略文件
├── main.py               # 应用入口
├── pyproject.toml        # 项目配置
└── README.md             # 项目说明
```

## 快速开始

### 1. 环境准备

确保您的系统已安装Python 3.9+和uv：

```bash
# 安装uv (如果尚未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆项目

```bash
git clone <repository-url>
cd smart-custom
```

### 3. 配置环境变量

复制并编辑环境变量文件：

```bash
cp .env.example .env
```

编辑`.env`文件，添加您的OpenAI API密钥：

```
OPENAI_API_KEY=your_openai_api_key_here
API_PORT=8001
```

### 4. 安装依赖

```bash
uv sync
```

### 5. 运行应用

```bash
uv run python main.py
```

应用将在 `http://localhost:8001` 启动。

## API文档

启动应用后，可以通过以下地址访问API文档：

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## API使用示例

### 基本对话

```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好，请介绍一下你的功能"}'
```

### 订单查询

```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "我想查询订单ORD202311003的状态"}'
```

### 退款申请

```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "我想申请退款，订单号是ORD202311005，因为不想要了"}'
```

### 发票生成

```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "请为订单ORD202311003开具发票"}'
```

### 热更新功能

#### 模型热更新

```bash
# 从环境变量重新加载模型配置
curl -X POST "http://localhost:8001/admin/model/reload"
```

#### 插件热重载

```bash
# 重新加载所有插件
curl -X POST "http://localhost:8001/admin/plugins/reload"
```

#### 服务状态检查

```bash
# 获取服务状态
curl -X GET "http://localhost:8001/admin/status"
```

## 开发指南

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=src --cov-report=html

# 运行热更新功能测试
uv run python tests/test_hot_update.py
```

### 代码格式化

```bash
# 使用ruff格式化代码
uv run ruff format src/

# 使用black格式化代码
uv run black src/
```

### 代码检查

```bash
# 使用ruff检查代码
uv run ruff check src/

# 使用mypy进行类型检查
uv run mypy src/
```

### 使用Makefile

项目提供了Makefile来简化常用操作：

```bash
# 安装依赖
make install

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format

# 运行应用
make run
```

## 热更新功能详解

本项目的热更新功能允许在不重启服务的情况下更新模型和插件，同时保持现有会话的连续性。

### 实现原理

1. **模型热更新**：通过创建新的LangGraph实例替换旧实例，实现模型配置的更新
2. **插件热重载**：通过重新导入插件模块，实现插件代码的更新
3. **会话隔离**：新会话使用更新后的配置，而旧会话继续使用原有配置直到自然结束

### 测试验证

项目提供了完整的热更新测试脚本(`tests/test_hot_update.py`)，验证以下功能：

- 服务健康检查
- 会话创建和对话历史构建
- 模型热更新功能
- 插件热重载功能
- 会话上下文保留
- 会话历史检索

运行测试：

```bash
uv run python tests/test_hot_update.py
```

## 部署

### Docker部署

```bash
# 构建Docker镜像
docker build -t smart-custom-api .

# 运行容器
docker run -p 8001:8001 --env-file .env smart-custom-api
```

### 云平台部署

本项目可以轻松部署到各种云平台，如：

- Heroku
- AWS Lambda
- Google Cloud Functions
- Azure Functions

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件至：[your-email@example.com]

## 更新日志

### v0.2.0 (2023-11-10)

- 添加热更新功能，支持模型和插件的不重启更新
- 实现会话隔离机制，确保热更新不影响现有会话
- 添加发票生成工具
- 完善测试覆盖，特别是热更新功能的测试
- 优化项目结构和代码组织

### v0.1.0 (2023-11-01)

- 初始版本发布
- 实现基本对话功能
- 添加订单查询功能
- 添加退款申请功能
- 完善API文档和测试