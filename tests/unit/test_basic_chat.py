#!/usr/bin/env python3
"""
测试基础聊天服务的时间推断功能
"""
import sys
import os
# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.basic_chat_service import basic_chat_service

def test_time_inference():
    # 测试时间推断
    time_result = basic_chat_service.infer_time("昨天")
    print("时间推断结果:", time_result)
    
    # 测试聊天功能
    chat_result = basic_chat_service.chat("我昨天下的单，什么时候能到货？")
    print("\n聊天结果:")
    print("成功:", chat_result["success"])
    print("响应:", chat_result["response"])
    print("时间推断:", chat_result.get("time_inference"))

if __name__ == "__main__":
    test_time_inference()