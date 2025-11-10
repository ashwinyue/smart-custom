"""
订单查询工具
"""
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class OrderQueryTool:
    """订单查询工具类"""
    
    def __init__(self):
        # 模拟订单数据库
        self.orders_db = {
            "ORD202311001": {
                "order_id": "ORD202311001",
                "status": "已发货",
                "product_name": "智能手表",
                "order_date": "2023-11-05",
                "estimated_delivery": "2023-11-08",
                "tracking_number": "SF1234567890",
                "logistics_company": "顺丰快递",
                "logistics_status": "运输中",
                "current_location": "上海转运中心"
            },
            "ORD202311002": {
                "order_id": "ORD202311002",
                "status": "已签收",
                "product_name": "无线耳机",
                "order_date": "2023-11-03",
                "delivery_date": "2023-11-06",
                "tracking_number": "YT9876543210",
                "logistics_company": "圆通快递",
                "logistics_status": "已签收",
                "current_location": "已送达"
            },
            "ORD202311003": {
                "order_id": "ORD202311003",
                "status": "处理中",
                "product_name": "智能音箱",
                "order_date": "2023-11-07",
                "estimated_delivery": "2023-11-12",
                "tracking_number": None,
                "logistics_company": None,
                "logistics_status": "仓库处理中",
                "current_location": "北京仓库"
            }
        }
    
    def query_order(self, order_id: str) -> Dict[str, Any]:
        """
        查询订单信息
        
        Args:
            order_id: 订单号
            
        Returns:
            包含订单信息的字典
        """
        # 模拟查询延迟
        import time
        time.sleep(0.5)
        
        # 查询订单
        order_info = self.orders_db.get(order_id)
        
        if order_info:
            return {
                "success": True,
                "order_info": order_info
            }
        else:
            return {
                "success": False,
                "error": f"订单号 {order_id} 不存在，请检查订单号是否正确"
            }
    
    def get_order_status_description(self, order_info: Dict[str, Any]) -> str:
        """
        获取订单状态描述
        
        Args:
            order_info: 订单信息
            
        Returns:
            订单状态描述文本
        """
        status = order_info.get("status", "")
        order_id = order_info.get("order_id", "")
        product_name = order_info.get("product_name", "")
        
        if status == "已发货":
            tracking_number = order_info.get("tracking_number", "")
            logistics_company = order_info.get("logistics_company", "")
            estimated_delivery = order_info.get("estimated_delivery", "")
            current_location = order_info.get("current_location", "")
            
            return (f"您的订单 {order_id}（{product_name}）已发货，物流公司：{logistics_company}，"
                    f"运单号：{tracking_number}，当前位置：{current_location}，"
                    f"预计送达时间：{estimated_delivery}。")
        
        elif status == "已签收":
            delivery_date = order_info.get("delivery_date", "")
            return (f"您的订单 {order_id}（{product_name}）已于 {delivery_date} 签收成功。"
                    f"感谢您的购买，如有问题请联系客服。")
        
        elif status == "处理中":
            estimated_delivery = order_info.get("estimated_delivery", "")
            current_location = order_info.get("current_location", "")
            return (f"您的订单 {order_id}（{product_name}）正在{current_location}处理中，"
                    f"预计 {estimated_delivery} 发货，请耐心等待。")
        
        else:
            return f"您的订单 {order_id} 当前状态为：{status}，如需了解更多信息请联系客服。"

# 创建全局订单查询工具实例
order_query_tool = OrderQueryTool()