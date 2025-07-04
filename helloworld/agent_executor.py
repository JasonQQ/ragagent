from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import Message, Part
import uuid


class HelloWorldAgent:
    """负责生成问候语的简单 Agent。"""
    async def invoke(self, user_message: str) -> str:
        return f"Hello World! You said: {user_message}"

class EchoAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = HelloWorldAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        user_message = ""
        if context and context.message and context.message.parts:
            user_message = context.message.parts[0].root.text
        reply_text = await self.agent.invoke(user_message)
        reply = Message(
            messageId=str(uuid.uuid4()),
            role="agent",
            parts=[Part(text=reply_text)]
        )
        await event_queue.enqueue_event(reply)

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        # 简单实现：直接返回取消状态
        pass 

    async def stream(self, context: RequestContext, event_queue: EventQueue):
        """
        流式推送消息示例：分3段推送，最后一段为最终消息。
        """
        import asyncio
        user_message = ""
        if context and context.message and context.message.parts:
            user_message = context.message.parts[0].root.text
        # 分段推送
        for i in range(3):
            part_text = f"分段消息 {i+1}: {user_message}"
            reply = Message(
                messageId=str(uuid.uuid4()),
                role="agent",
                parts=[Part(text=part_text)]
            )
            await event_queue.enqueue_event(reply)
            await asyncio.sleep(0.5)  # 模拟延迟
        # 最终消息
        final_text = await self.agent.invoke(user_message)
        reply = Message(
            messageId=str(uuid.uuid4()),
            role="agent",
            parts=[Part(text=final_text + " (流式结束)")]
        )
        await event_queue.enqueue_event(reply) 