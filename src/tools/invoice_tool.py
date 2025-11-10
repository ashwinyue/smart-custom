"""
发票开具工具

此工具用于处理发票开具相关的请求，包括创建发票、查询发票状态和获取发票详情。
"""

import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from src.utils.logger import app_logger

class InvoiceManager:
    """发票管理器"""
    
    def __init__(self):
        """初始化发票管理器"""
        self.invoices = {}  # 存储发票数据
        self.invoice_counter = 1000  # 发票计数器
    
    def generate_invoice_id(self) -> str:
        """生成发票ID"""
        self.invoice_counter += 1
        return f"INV{datetime.now().strftime('%Y%m%d')}{self.invoice_counter:04d}"
    
    def create_invoice(
        self, 
        customer_name: str, 
        customer_tax_id: str, 
        items: List[Dict[str, Any]], 
        issue_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建发票
        
        Args:
            customer_name: 客户名称
            customer_tax_id: 客户税号
            items: 商品列表，每个商品包含名称、数量、单价等信息
            issue_date: 开票日期，格式为YYYY-MM-DD，默认为当前日期
            
        Returns:
            包含发票信息的字典
        """
        try:
            # 验证输入参数
            if not customer_name or not customer_tax_id:
                return {
                    "success": False,
                    "error": "客户名称和税号不能为空"
                }
            
            if not items or len(items) == 0:
                return {
                    "success": False,
                    "error": "商品列表不能为空"
                }
            
            # 验证商品信息
            for item in items:
                if "name" not in item or "quantity" not in item or "unit_price" not in item:
                    return {
                        "success": False,
                        "error": "商品信息不完整，必须包含名称、数量和单价"
                    }
                
                if item["quantity"] <= 0 or item["unit_price"] <= 0:
                    return {
                        "success": False,
                        "error": "商品数量和单价必须大于0"
                    }
            
            # 处理开票日期
            if issue_date:
                try:
                    parsed_date = datetime.strptime(issue_date, "%Y-%m-%d")
                except ValueError:
                    return {
                        "success": False,
                        "error": "开票日期格式不正确，请使用YYYY-MM-DD格式"
                    }
            else:
                parsed_date = datetime.now()
                issue_date = parsed_date.strftime("%Y-%m-%d")
            
            # 生成发票ID
            invoice_id = self.generate_invoice_id()
            
            # 计算总金额
            total_amount = 0.0
            for item in items:
                item_total = item["quantity"] * item["unit_price"]
                item["total"] = round(item_total, 2)
                total_amount += item_total
            
            total_amount = round(total_amount, 2)
            
            # 计算税额（假设税率为13%）
            tax_rate = 0.13
            tax_amount = round(total_amount * tax_rate, 2)
            
            # 计算价税合计
            total_with_tax = round(total_amount + tax_amount, 2)
            
            # 创建发票记录
            invoice = {
                "invoice_id": invoice_id,
                "customer_name": customer_name,
                "customer_tax_id": customer_tax_id,
                "items": items,
                "issue_date": issue_date,
                "due_date": (parsed_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "subtotal": total_amount,
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "total_with_tax": total_with_tax,
                "status": "issued",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # 保存发票
            self.invoices[invoice_id] = invoice
            
            app_logger.info(f"创建发票成功: {invoice_id}")
            
            return {
                "success": True,
                "invoice_id": invoice_id,
                "message": f"发票 {invoice_id} 创建成功",
                "invoice": invoice
            }
        except Exception as e:
            app_logger.error(f"创建发票时出错: {str(e)}")
            return {
                "success": False,
                "error": f"创建发票时出错: {str(e)}"
            }
    
    def query_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """
        查询发票状态
        
        Args:
            invoice_id: 发票ID
            
        Returns:
            包含发票状态的字典
        """
        try:
            if not invoice_id:
                return {
                    "success": False,
                    "error": "发票ID不能为空"
                }
            
            # 查找发票
            invoice = self.invoices.get(invoice_id)
            
            if not invoice:
                return {
                    "success": False,
                    "error": f"发票 {invoice_id} 不存在"
                }
            
            # 获取状态描述
            status_descriptions = {
                "issued": "已开具",
                "sent": "已发送",
                "paid": "已支付",
                "overdue": "已逾期",
                "cancelled": "已取消"
            }
            
            status_description = status_descriptions.get(invoice["status"], invoice["status"])
            
            app_logger.info(f"查询发票状态: {invoice_id}, 状态: {invoice['status']}")
            
            return {
                "success": True,
                "invoice_id": invoice_id,
                "status": invoice["status"],
                "status_description": status_description,
                "issue_date": invoice["issue_date"],
                "due_date": invoice["due_date"],
                "total_with_tax": invoice["total_with_tax"]
            }
        except Exception as e:
            app_logger.error(f"查询发票状态时出错: {str(e)}")
            return {
                "success": False,
                "error": f"查询发票状态时出错: {str(e)}"
            }
    
    def get_invoice_details(self, invoice_id: str) -> Dict[str, Any]:
        """
        获取发票详情
        
        Args:
            invoice_id: 发票ID
            
        Returns:
            包含发票详情的字典
        """
        try:
            if not invoice_id:
                return {
                    "success": False,
                    "error": "发票ID不能为空"
                }
            
            # 查找发票
            invoice = self.invoices.get(invoice_id)
            
            if not invoice:
                return {
                    "success": False,
                    "error": f"发票 {invoice_id} 不存在"
                }
            
            app_logger.info(f"获取发票详情: {invoice_id}")
            
            return {
                "success": True,
                "invoice": invoice
            }
        except Exception as e:
            app_logger.error(f"获取发票详情时出错: {str(e)}")
            return {
                "success": False,
                "error": f"获取发票详情时出错: {str(e)}"
            }
    
    def update_invoice_status(self, invoice_id: str, new_status: str) -> Dict[str, Any]:
        """
        更新发票状态
        
        Args:
            invoice_id: 发票ID
            new_status: 新状态
            
        Returns:
            包含更新结果的字典
        """
        try:
            if not invoice_id:
                return {
                    "success": False,
                    "error": "发票ID不能为空"
                }
            
            if not new_status:
                return {
                    "success": False,
                    "error": "新状态不能为空"
                }
            
            # 验证状态
            valid_statuses = ["issued", "sent", "paid", "overdue", "cancelled"]
            if new_status not in valid_statuses:
                return {
                    "success": False,
                    "error": f"无效的状态，有效状态为: {', '.join(valid_statuses)}"
                }
            
            # 查找发票
            invoice = self.invoices.get(invoice_id)
            
            if not invoice:
                return {
                    "success": False,
                    "error": f"发票 {invoice_id} 不存在"
                }
            
            # 更新状态
            old_status = invoice["status"]
            invoice["status"] = new_status
            invoice["updated_at"] = datetime.now().isoformat()
            
            app_logger.info(f"更新发票状态: {invoice_id}, 从 {old_status} 到 {new_status}")
            
            return {
                "success": True,
                "invoice_id": invoice_id,
                "message": f"发票 {invoice_id} 状态已从 {old_status} 更新为 {new_status}",
                "old_status": old_status,
                "new_status": new_status
            }
        except Exception as e:
            app_logger.error(f"更新发票状态时出错: {str(e)}")
            return {
                "success": False,
                "error": f"更新发票状态时出错: {str(e)}"
            }
    
    def list_invoices(
        self, 
        customer_name: Optional[str] = None, 
        status: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        列出发票
        
        Args:
            customer_name: 客户名称（可选）
            status: 发票状态（可选）
            limit: 返回的最大数量
            
        Returns:
            包含发票列表的字典
        """
        try:
            # 筛选发票
            filtered_invoices = []
            
            for invoice_id, invoice in self.invoices.items():
                # 按客户名称筛选
                if customer_name and customer_name.lower() not in invoice["customer_name"].lower():
                    continue
                
                # 按状态筛选
                if status and invoice["status"] != status:
                    continue
                
                # 添加到结果列表
                filtered_invoices.append({
                    "invoice_id": invoice_id,
                    "customer_name": invoice["customer_name"],
                    "issue_date": invoice["issue_date"],
                    "due_date": invoice["due_date"],
                    "total_with_tax": invoice["total_with_tax"],
                    "status": invoice["status"]
                })
            
            # 按开票日期降序排序
            filtered_invoices.sort(key=lambda x: x["issue_date"], reverse=True)
            
            # 限制结果数量
            if limit > 0:
                filtered_invoices = filtered_invoices[:limit]
            
            app_logger.info(f"列出发票，筛选条件: 客户={customer_name}, 状态={status}, 返回数量={len(filtered_invoices)}")
            
            return {
                "success": True,
                "invoices": filtered_invoices,
                "total_count": len(filtered_invoices)
            }
        except Exception as e:
            app_logger.error(f"列出发票时出错: {str(e)}")
            return {
                "success": False,
                "error": f"列出发票时出错: {str(e)}"
            }

# 创建全局发票管理器实例
invoice_manager = InvoiceManager()

# 工具函数

def create_invoice(
    customer_name: str, 
    customer_tax_id: str, 
    items: List[Dict[str, Any]], 
    issue_date: Optional[str] = None
) -> str:
    """
    创建发票
    
    Args:
        customer_name: 客户名称
        customer_tax_id: 客户税号
        items: 商品列表，每个商品包含名称、数量、单价等信息
        issue_date: 开票日期，格式为YYYY-MM-DD，默认为当前日期
        
    Returns:
        创建结果的消息
    """
    result = invoice_manager.create_invoice(customer_name, customer_tax_id, items, issue_date)
    
    if result["success"]:
        return f"发票创建成功！发票ID: {result['invoice_id']}，总金额: {result['invoice']['total_with_tax']}元"
    else:
        return f"发票创建失败: {result['error']}"

def query_invoice_status(invoice_id: str) -> str:
    """
    查询发票状态
    
    Args:
        invoice_id: 发票ID
        
    Returns:
        发票状态信息
    """
    result = invoice_manager.query_invoice_status(invoice_id)
    
    if result["success"]:
        return (f"发票 {result['invoice_id']} 的状态为: {result['status_description']}，"
                f"开票日期: {result['issue_date']}，到期日: {result['due_date']}，"
                f"金额: {result['total_with_tax']}元")
    else:
        return f"查询发票状态失败: {result['error']}"

def get_invoice_details(invoice_id: str) -> str:
    """
    获取发票详情
    
    Args:
        invoice_id: 发票ID
        
    Returns:
        发票详情信息
    """
    result = invoice_manager.get_invoice_details(invoice_id)
    
    if result["success"]:
        invoice = result['invoice']
        items_str = "\n".join([
            f"- {item['name']}: {item['quantity']} × {item['unit_price']}元 = {item['total']}元"
            for item in invoice['items']
        ])
        
        return (f"发票详情:\n"
                f"发票ID: {invoice['invoice_id']}\n"
                f"客户名称: {invoice['customer_name']}\n"
                f"客户税号: {invoice['customer_tax_id']}\n"
                f"开票日期: {invoice['issue_date']}\n"
                f"到期日: {invoice['due_date']}\n"
                f"商品列表:\n{items_str}\n"
                f"小计: {invoice['subtotal']}元\n"
                f"税率: {invoice['tax_rate']*100}%\n"
                f"税额: {invoice['tax_amount']}元\n"
                f"价税合计: {invoice['total_with_tax']}元\n"
                f"状态: {invoice['status']}")
    else:
        return f"获取发票详情失败: {result['error']}"

def update_invoice_status(invoice_id: str, new_status: str) -> str:
    """
    更新发票状态
    
    Args:
        invoice_id: 发票ID
        new_status: 新状态
        
    Returns:
        更新结果的消息
    """
    result = invoice_manager.update_invoice_status(invoice_id, new_status)
    
    if result["success"]:
        return result["message"]
    else:
        return f"更新发票状态失败: {result['error']}"

def list_invoices(
    customer_name: Optional[str] = None, 
    status: Optional[str] = None,
    limit: int = 10
) -> str:
    """
    列出发票
    
    Args:
        customer_name: 客户名称（可选）
        status: 发票状态（可选）
        limit: 返回的最大数量
        
    Returns:
        发票列表信息
    """
    result = invoice_manager.list_invoices(customer_name, status, limit)
    
    if result["success"]:
        if not result["invoices"]:
            return "没有找到符合条件的发票"
        
        invoices_str = "\n".join([
            f"- {inv['invoice_id']}: {inv['customer_name']}, {inv['issue_date']}, {inv['total_with_tax']}元, {inv['status']}"
            for inv in result["invoices"]
        ])
        
        return f"找到 {result['total_count']} 张发票:\n{invoices_str}"
    else:
        return f"列出发票失败: {result['error']}"