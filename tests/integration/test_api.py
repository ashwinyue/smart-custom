import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Smart Custom API" in response.json()["message"]

def test_health_endpoint():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint():
    """测试聊天端点"""
    response = client.post(
        "/chat",
        json={"message": "你好，请介绍一下你的功能"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "response" in data
    assert "conversation_history" not in data  # 确认响应中不包含对话历史

def test_order_query():
    """测试订单查询功能"""
    response = client.post(
        "/chat",
        json={"message": "我想查询订单ORD202311003的状态"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "智能音箱" in data["response"]
    assert "北京仓库" in data["response"]

def test_refund_request():
    """测试退款申请功能"""
    response = client.post(
        "/chat",
        json={"message": "我想申请退款，订单号是ORD202311005，因为不想要了"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "退款申请" in data["response"]
    assert "REF" in data["response"]