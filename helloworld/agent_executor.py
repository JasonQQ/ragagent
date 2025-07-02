from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import Message, Part
import uuid

class EchoAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        user_message = ""
        if context and context.message and context.message.parts:
            user_message = context.message.parts[0].root.text
        reply_text = f"Hello World! You said: {user_message}"
        reply = Message(
            messageId=str(uuid.uuid4()),
            role="agent",
            parts=[Part(text=reply_text)]
        )
        await event_queue.enqueue_event(reply)

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        # 简单实现：直接返回取消状态
        pass 