import asyncio
import logging
import httpx
import argparse
from a2a.client.client import A2ACardResolver, A2AClient
from a2a.types import SendMessageRequest, Message, Part, SendStreamingMessageRequest

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description="A2A test client")
    parser.add_argument('--access-token', type=str, default=None, help='Access token for authenticated extended agent card')
    return parser.parse_args()

async def main():
    args = parse_args()
    base_url = "http://localhost:8000"
    access_token = args.access_token

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(httpx_client, base_url)

        # 先获取公共 AgentCard
        public_agent_card = await resolver.get_agent_card()
        logging.info("已获取 public agent card")

        # 判断是否支持扩展卡
        agent_card = public_agent_card
        if getattr(public_agent_card, 'supportsAuthenticatedExtendedCard', False) and access_token:
            agent_card = await resolver.get_agent_card(
                relative_card_path="/agent/authenticatedExtendedCard",
                http_kwargs={"headers": {"Authorization": f"Bearer {access_token}"}}
            )
            logging.info("已获取 extended agent card")
        else:
            if access_token:
                logging.info("access_token 已提供，但 agent 不支持扩展卡，继续使用 public agent card")
            else:
                logging.info("未提供 access_token，使用 public agent card")

        skills = agent_card.skills
        hello_skill_id = None
        extended_skill_id = None
        for skill in skills:
            logging.info(f"Skill id: {skill.id}, name: {getattr(skill, 'name', None)}, desc: {getattr(skill, 'description', None)}")
            if "hello" in skill.id:
                hello_skill_id = skill.id
            if "extended" in skill.id:
                extended_skill_id = skill.id

        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

        if hello_skill_id:
            hello_req = SendMessageRequest(
                id="test-hello-1",
                params={
                    "message": Message(
                        messageId="test-hello-1",
                        role="user",
                        parts=[Part(text="你好，普通问候测试")]
                    ),
                    "skillId": hello_skill_id
                }
            )
            hello_resp = await client.send_message(hello_req)
            logging.info(f"hello_skill 响应: {hello_resp}")

        if extended_skill_id:
            extended_req = SendMessageRequest(
                id="test-extended-1",
                params={
                    "message": Message(
                        messageId="test-extended-1",
                        role="user",
                        parts=[Part(text="你好，扩展问候测试")]
                    ),
                    "skillId": extended_skill_id
                }
            )
            extended_resp = await client.send_message(extended_req)
            logging.info(f"extended_skill 响应: {extended_resp}")

        # Streaming 消息测试
        if hello_skill_id:
            stream_req = SendStreamingMessageRequest(
                id="stream-hello-1",
                params={
                    "message": Message(
                        messageId="stream-hello-1",
                        role="user",
                        parts=[Part(text="你好，streaming 测试")]
                    ),
                    "skillId": hello_skill_id
                }
            )
            logging.info("开始 streaming 消息测试 (hello_skill)...")
            async for resp in client.send_message_streaming(stream_req):
                logging.info(f"streaming 响应: {resp}")
                # 可根据需要 break 或继续手动交互

if __name__ == "__main__":
    asyncio.run(main()) 