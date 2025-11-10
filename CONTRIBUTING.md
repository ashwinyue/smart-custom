# 贡献指南

感谢您对Smart Custom API项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 报告错误
- 提出新功能建议
- 提交代码改进
- 完善文档

## 开发环境设置

1. Fork 本仓库
2. 克隆您的Fork到本地：
   ```bash
   git clone https://github.com/your-username/smart-custom.git
   cd smart-custom
   ```
3. 添加上游仓库：
   ```bash
   git remote add upstream https://github.com/original-owner/smart-custom.git
   ```
4. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```
5. 安装依赖：
   ```bash
   uv sync
   ```
6. 安装预提交钩子：
   ```bash
   uv run pre-commit install
   ```

## 开发流程

1. 创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. 进行开发，确保代码符合项目规范
3. 运行测试：
   ```bash
   uv run pytest
   ```
4. 提交更改：
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```
5. 推送到您的Fork：
   ```bash
   git push origin feature/your-feature-name
   ```
6. 创建Pull Request

## 代码规范

- 遵循PEP 8代码风格
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 确保所有测试通过
- 保持代码简洁和可读性

## 提交信息规范

我们使用[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)规范：

- `feat:` 新功能
- `fix:` 修复错误
- `docs:` 文档更新
- `style:` 代码格式化（不影响功能）
- `refactor:` 重构代码
- `test:` 添加或修改测试
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加订单查询功能
fix: 修复API响应中的错误处理
docs: 更新README文档
```

## 测试指南

- 为新功能编写单元测试
- 确保测试覆盖率不降低
- 使用描述性的测试名称
- 测试边界条件和错误情况

## 文档贡献

- 确保文档清晰、准确、完整
- 使用中文编写文档
- 更新相关的API文档
- 添加必要的代码示例

## 问题报告

使用GitHub Issues报告问题时，请提供：

- 问题的详细描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（操作系统、Python版本等）
- 相关错误日志

## 许可证

通过贡献代码，您同意您的贡献将在与项目相同的MIT许可证下授权。

## 联系方式

如有任何问题，请通过以下方式联系：

- 创建GitHub Issue
- 发送邮件至：[your-email@example.com]

感谢您的贡献！