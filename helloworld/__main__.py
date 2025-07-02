from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    Message,
    Part
)
from dotenv import load_dotenv
import asyncio
import uvicorn
import uuid
from helloworld.agent_executor import EchoAgentExecutor

# 加载环境变量
load_dotenv()

# 定义 AgentSkill
hello_skill = AgentSkill(
    id="hello_world",
    name="Hello World",
    description="Returns a hello world greeting.",
    tags=["greeting"],
    examples=["hi", "hello world"]
)

# 定义 AgentCard
agent_card = AgentCard(
    name="HelloWorldAgent",
    description="A simple agent that returns hello world.",
    url="http://localhost:8000",  # 启动时请确保端口一致
    version="0.1.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(),
    skills=[hello_skill]
)

# 创建 EchoAgentExecutor 实例
agent_executor = EchoAgentExecutor()

# 创建 A2AStarletteApplication
app = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore()
    )
).build()

if __name__ == "__main__":
    uvicorn.run("helloworld.__main__:app", host="0.0.0.0", port=8000, reload=True) 