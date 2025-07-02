# Hello World A2A Agent 示例

> 本项目代码由 [Cursor AI 代码助手](https://www.cursor.so/) 自动生成与重构。

本项目基于谷歌 A2A (Agent-to-Agent) SDK，演示了如何创建一个简单的智能代理服务器，能够响应用户消息并返回问候语。

## 依赖环境
- Python >= 3.10
- 依赖包见 `pyproject.toml`（Poetry 管理）

## 安装依赖
```bash
poetry install
```

## 运行方式
```bash
poetry run uvicorn helloworld.__main__:app --reload
```

## 主要依赖说明
| 包名 | 版本 | 用途 |
| ---- | ---- | ---- |
| a2a-sdk | >= 0.2.5 | A2A 核心 SDK，提供代理框架 |
| uvicorn | >= 0.34.2 | ASGI 服务器 |
| click | >= 8.1.8 | 命令行工具 |
| httpx | >= 0.28.1 | 异步 HTTP 客户端 |
| pydantic | >= 2.11.4 | 数据验证和序列化 |
| python-dotenv | >= 1.1.0 | 环境变量管理 |
| langchain-google-genai | >= 2.1.4 | Google 生成式 AI 集成 |
| langgraph | >= 0.4.1 | 语言图处理框架 |

## 目录结构
- `helloworld/__main__.py`：主应用入口
- `helloworld/agent_executor.py`：EchoAgentExecutor 实现
- `pyproject.toml`：Poetry 依赖与项目配置
- `test_main.py`：集成测试 