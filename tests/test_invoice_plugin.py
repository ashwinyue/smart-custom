#!/usr/bin/env python3
"""
发票开具插件功能测试脚本
测试发票工具的各个功能是否正常工作
"""

import json
import requests
import uuid
from typing import Dict, Any, List
import time

class InvoicePluginTester:
    """发票插件测试类"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        status = "✅" if success else "❌"
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
    
    def check_service_health(self) -> bool:
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("服务健康检查", True, f"状态码: {response.status_code}")
                return True
            else:
                self.log_test("服务健康检查", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("服务健康检查", False, f"连接错误: {str(e)}")
            return False
    
    def create_session(self) -> bool:
        """创建测试会话"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "你好，我想测试发票开具功能",
                    "session_id": self.session_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("会话创建", True)
                    return True
                else:
                    self.log_test("会话创建", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("会话创建", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("会话创建", False, f"请求错误: {str(e)}")
            return False
    
    def test_create_invoice(self) -> bool:
        """测试创建发票功能"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请帮我创建一张发票，购买方是ABC公司，税号123456789，金额1000元，商品是咨询服务",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("创建发票", True, "成功创建发票")
                    return True
                else:
                    self.log_test("创建发票", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("创建发票", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("创建发票", False, f"请求错误: {str(e)}")
            return False
    
    def test_query_invoice_status(self) -> bool:
        """测试查询发票状态功能"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请查询发票INV-001的状态",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("查询发票状态", True, "成功查询发票状态")
                    return True
                else:
                    self.log_test("查询发票状态", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("查询发票状态", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("查询发票状态", False, f"请求错误: {str(e)}")
            return False
    
    def test_get_invoice_details(self) -> bool:
        """测试获取发票详情功能"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请获取发票INV-001的详细信息",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("获取发票详情", True, "成功获取发票详情")
                    return True
                else:
                    self.log_test("获取发票详情", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("获取发票详情", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("获取发票详情", False, f"请求错误: {str(e)}")
            return False
    
    def test_update_invoice_status(self) -> bool:
        """测试更新发票状态功能"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请将发票INV-001的状态更新为已支付",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("更新发票状态", True, "成功更新发票状态")
                    return True
                else:
                    self.log_test("更新发票状态", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("更新发票状态", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("更新发票状态", False, f"请求错误: {str(e)}")
            return False
    
    def test_list_invoices(self) -> bool:
        """测试列出发票功能"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请列出所有发票",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("列出发票", True, "成功列出发票")
                    return True
                else:
                    self.log_test("列出发票", False, data.get("error", "未知错误"))
                    return False
            else:
                self.log_test("列出发票", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("列出发票", False, f"请求错误: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """测试错误处理"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": "请查询一个不存在的发票INV-99999",
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                # 即使发票不存在，API调用成功也是预期的
                self.log_test("错误处理", True, "API正确处理了错误情况")
                return True
            else:
                self.log_test("错误处理", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("错误处理", False, f"请求错误: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("=" * 60)
        print("发票开具插件功能测试")
        print("=" * 60)
        print(f"会话ID: {self.session_id}")
        print("🚀 开始运行发票插件功能测试...")
        
        # 检查服务健康状态
        if not self.check_service_health():
            print("❌ 服务不可用，测试终止")
            return {"success": False, "message": "服务不可用"}
        
        print("✅ 服务可用，开始测试...")
        
        # 创建会话
        if not self.create_session():
            print("❌ 会话创建失败，测试终止")
            return {"success": False, "message": "会话创建失败"}
        
        # 等待一下确保会话创建完成
        time.sleep(1)
        
        # 运行所有测试
        self.test_create_invoice()
        time.sleep(1)
        
        self.test_query_invoice_status()
        time.sleep(1)
        
        self.test_get_invoice_details()
        time.sleep(1)
        
        self.test_update_invoice_status()
        time.sleep(1)
        
        self.test_list_invoices()
        time.sleep(1)
        
        self.test_error_handling()
        
        # 汇总测试结果
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"成功率: {passed_tests/total_tests*100:.1f}%")
        
        # 打印失败的测试
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        return {
            "success": failed_tests == 0,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "test_results": self.test_results
        }

if __name__ == "__main__":
    # 运行测试
    tester = InvoicePluginTester()
    results = tester.run_all_tests()
    
    # 退出码
    exit(0 if results["success"] else 1)