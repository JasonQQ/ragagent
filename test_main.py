import pytest
import httpx
import asyncio
import subprocess
import time

SERVER_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def start_server():
    # 启动 uvicorn 服务
    proc = subprocess.Popen([
        "uvicorn", "helloworld.__main__:app", "--host", "127.0.0.1", "--port", "8000"
    ])
    # 等待服务启动
    time.sleep(2)
    yield
    proc.terminate()
    proc.wait()

@pytest.mark.asyncio
async def test_root():
    async with httpx.AsyncClient(base_url=SERVER_URL) as ac:
        resp = await ac.get("/.well-known/agent.json")
        assert resp.status_code == 200
        assert resp.json()["name"].startswith("HelloWorldAgent")

@pytest.mark.asyncio
async def test_a2a_message():
    async with httpx.AsyncClient(base_url=SERVER_URL) as ac:
        data = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "message/send",
            "params": {
                "message": {
                    "messageId": "msg-1",
                    "role": "user",
                    "parts": [{"text": "你好"}]
                }
            }
        }
        resp = await ac.post("/", json=data)
        assert resp.status_code == 200
        result = resp.json()
        assert "Hello World!" in str(result)

@pytest.mark.asyncio
async def test_hello_world_message():
    async with httpx.AsyncClient(base_url=SERVER_URL) as ac:
        data = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "message/send",
            "params": {
                "message": {
                    "messageId": "msg-2",
                    "role": "user",
                    "parts": [{"text": "测试消息"}]
                }
            }
        }
        resp = await ac.post("/", json=data)
        assert resp.status_code == 200
        result = resp.json()
        assert "Hello World!" in str(result) 