#!/usr/bin/env python3
"""
热更新功能测试脚本
测试热更新后旧会话不受影响
"""

import json
import requests
import uuid
import time
from typing import Dict, Any, List

# 配置
BASE_URL = "http://localhost:8001"
USER_ID = "test_user"
SESSION_ID = str(uuid.uuid4())

def test_health_check() -> bool:
    """测试服务健康检查"""
    print("🔍 测试服务健康检查...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ 服务健康检查成功，状态码: {response.status_code}")
            return True
        else:
            print(f"   ❌ 服务健康检查失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 服务健康检查异常: {str(e)}")
        return False

# 测试会话创建
def test_create_session():
    """测试会话创建"""
    print("\n=== 测试1: 会话创建 ===")
    
    # 发送消息创建会话
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"user_id": USER_ID, "message": "你好，我想创建一个新会话"}
    )
    
    if response.status_code == 200:
        data = response.json()
        global SESSION_ID
        SESSION_ID = data.get("session_id")
        print(f"✓ 会话创建成功，会话ID: {SESSION_ID}")
        return True
    else:
        print(f"✗ 会话创建失败: {response.status_code}")
        return False

def test_build_conversation_history() -> bool:
    """测试构建对话历史"""
    print("💬 测试构建对话历史...")
    
    try:
        messages = [
            "我的名字是张三",
            "我在一家科技公司工作",
            "我最喜欢的编程语言是Python",
            "我正在开发一个聊天机器人项目"
        ]
        
        for i, message in enumerate(messages):
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "user_id": USER_ID,
                    "message": message,
                    "session_id": SESSION_ID
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"   ❌ 消息 {i+1} 发送失败")
                return False
            
            data = response.json()
            if not data.get("success"):
                print(f"   ❌ 消息 {i+1} 处理失败: {data.get('error')}")
                return False
            
            time.sleep(0.5)  # 避免请求过快
        
        print("   ✅ 对话历史构建成功，发送了4条消息")
        return True
    except Exception as e:
        print(f"   ❌ 对话历史构建异常: {str(e)}")
        return False

def test_model_hot_update() -> bool:
    """测试模型热更新功能"""
    print("🔥 测试模型热更新功能...")
    
    try:
        # 获取更新前的模型状态
        response = requests.get(f"{BASE_URL}/admin/status")
        if response.status_code != 200:
            print(f"   ❌ 获取服务状态失败: {response.status_code}")
            return False
        
        status_data = response.json()
        if not status_data.get("success", False):
            print(f"   ❌ 获取服务状态失败: {status_data.get('error', '未知错误')}")
            return False
            
        # 从环境变量重新加载模型配置
        response = requests.post(f"{BASE_URL}/admin/model/reload")
        if response.status_code != 200:
            print(f"   ❌ 模型热更新失败: {response.status_code}")
            return False
        
        result = response.json()
        if result.get("success", False):
            print("   ✅ 模型热更新成功")
            return True
        else:
            print(f"   ❌ 模型热更新失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 模型热更新异常: {str(e)}")
        return False

def test_plugin_hot_reload() -> bool:
    """测试插件热重载功能"""
    print("🔌 测试插件热重载功能...")
    
    try:
        # 获取重载前的插件状态
        response = requests.get(f"{BASE_URL}/admin/status")
        if response.status_code != 200:
            print(f"   ❌ 获取服务状态失败: {response.status_code}")
            return False
        
        status_data = response.json()
        if not status_data.get("success", False):
            print(f"   ❌ 获取服务状态失败: {status_data.get('error', '未知错误')}")
            return False
        
        # 重新加载所有插件
        response = requests.post(f"{BASE_URL}/admin/plugins/reload")
        if response.status_code != 200:
            print(f"   ❌ 插件热重载失败: {response.status_code}")
            return False
        
        result = response.json()
        if result.get("success", False):
            print("   ✅ 插件热重载成功")
            return True
        else:
            print(f"   ❌ 插件热重载失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 插件热重载异常: {str(e)}")
        return False

def test_session_context_preservation():
    """测试会话上下文保留"""
    print("\n=== 测试6: 会话上下文保留 ===")
    
    # 发送一条引用之前信息的消息
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "user_id": USER_ID,
            "message": "你还记得我的名字吗？",
            "session_id": SESSION_ID
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("✓ 会话上下文保留测试成功")
            print(f"  AI响应: {data.get('response', '')[:50]}...")
            return True
        else:
            print(f"✗ 会话上下文保留测试失败: {data.get('error', '未知错误')}")
            return False
    else:
        print(f"✗ 会话上下文保留测试失败，状态码: {response.status_code}")
        return False

def test_session_history_retrieval():
    """测试会话历史检索"""
    print("\n=== 测试7: 会话历史检索 ===")
    
    # 获取会话历史
    response = requests.post(
        f"{BASE_URL}/session/history",
        json={
            "user_id": USER_ID,
            "session_id": SESSION_ID
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            # 从session对象中获取messages
            session_data = data.get("session", {})
            messages = session_data.get("messages", [])
            print(f"✓ 会话历史检索成功，共 {len(messages)} 条消息")
            
            # 验证消息数量是否达到预期
            if len(messages) >= 6:  # 预期6条消息（3条用户消息 + 3条AI响应）
                print("✓ 消息数量符合预期")
                return True
            else:
                print(f"✗ 消息数量不符合预期，预期至少6条，实际{len(messages)}条")
                return False
        else:
            print(f"✗ 会话历史检索失败: {data.get('error', '未知错误')}")
            return False
    else:
        print(f"✗ 会话历史检索失败，状态码: {response.status_code}")
        return False

def main():
    """主测试函数"""
    print("🔥 开始热更新功能测试...")
    
    results = []
    
    # 1. 测试服务健康状态
    results.append(("服务健康检查", test_health_check()))
    
    # 2. 测试会话创建
    results.append(("会话创建", test_create_session()))
    
    # 3. 构建对话历史
    results.append(("对话历史构建", test_build_conversation_history()))
    
    # 4. 测试模型热更新
    results.append(("模型热更新", test_model_hot_update()))
    
    # 5. 测试插件热重载
    results.append(("插件热重载", test_plugin_hot_reload()))
    
    # 6. 测试会话上下文保留
    results.append(("会话上下文保留", test_session_context_preservation()))
    
    # 7. 测试会话历史检索
    results.append(("会话历史检索", test_session_history_retrieval()))
    
    # 输出测试结果
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\n总体结果: {passed}/{len(results)} 项测试通过 ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 热更新功能测试通过!")
    else:
        print("⚠️  热更新功能测试未完全通过，需要进一步调试。")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 热更新功能测试通过！")
        exit(0)
    else:
        print("\n❌ 热更新功能测试未通过！")
        exit(1)