# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 项目结构重组，遵循Python最佳实践
- 添加Docker支持
- 添加预提交钩子配置
- 完善项目文档

### Changed
- 从ChatResponse模型中移除conversation_history字段
- 精简API响应结构

### Fixed
- 修复对话历史记录问题

## [0.1.0] - 2023-11-10

### Added
- 初始版本发布
- 实现基于FastAPI的基本API框架
- 集成OpenAI GPT-3.5-turbo模型
- 实现智能对话功能
- 添加订单查询功能
- 添加退款申请功能
- 完善API文档和测试

### Changed
- 从通义千问API切换到OpenAI API
- 使用LangGraph替代LangChain的对话链

### Fixed
- 修复模型初始化问题
- 修复环境变量配置问题