"""
退款申请工具
"""
from typing import Dict, Any, List
from datetime import datetime
import uuid

class RefundRequestTool:
    """退款申请工具类"""
    
    def __init__(self):
        # 模拟退款申请数据库
        self.refunds_db = {}
        
        # 退款原因选项
        self.refund_reasons = [
            "商品质量问题",
            "商品与描述不符",
            "不想要了/买错了",
            "商品损坏",
            "发货延迟",
            "其他原因"
        ]
    
    def get_refund_reasons(self) -> List[str]:
        """
        获取退款原因选项
        
        Returns:
            退款原因列表
        """
        return self.refund_reasons
    
    def submit_refund_request(self, order_id: str, reason: str, description: str = "") -> Dict[str, Any]:
        """
        提交退款申请
        
        Args:
            order_id: 订单号
            reason: 退款原因
            description: 退款描述（可选）
            
        Returns:
            包含申请结果的字典
        """
        # 模拟处理延迟
        import time
        time.sleep(0.5)
        
        # 生成退款申请ID
        refund_id = f"REF{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # 创建退款申请记录
        refund_record = {
            "refund_id": refund_id,
            "order_id": order_id,
            "reason": reason,
            "description": description,
            "status": "处理中",
            "apply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_process_time": (datetime.now().replace(hour=23, minute=59, second=0)).strftime("%Y-%m-%d %H:%M:%S"),
            "refund_amount": None,  # 实际系统中会根据订单计算
            "process_result": None
        }
        
        # 保存到数据库
        self.refunds_db[refund_id] = refund_record
        
        return {
            "success": True,
            "refund_id": refund_id,
            "message": f"您的退款申请已提交，申请编号：{refund_id}，我们将在24小时内处理您的申请。"
        }
    
    def query_refund_status(self, refund_id: str) -> Dict[str, Any]:
        """
        查询退款申请状态
        
        Args:
            refund_id: 退款申请ID
            
        Returns:
            包含退款状态的字典
        """
        # 模拟查询延迟
        import time
        time.sleep(0.3)
        
        refund_record = self.refunds_db.get(refund_id)
        
        if refund_record:
            return {
                "success": True,
                "refund_info": refund_record
            }
        else:
            return {
                "success": False,
                "error": f"退款申请编号 {refund_id} 不存在，请检查编号是否正确"
            }
    
    def get_refund_status_description(self, refund_info: Dict[str, Any]) -> str:
        """
        获取退款状态描述
        
        Args:
            refund_info: 退款信息
            
        Returns:
            退款状态描述文本
        """
        refund_id = refund_info.get("refund_id", "")
        order_id = refund_info.get("order_id", "")
        status = refund_info.get("status", "")
        apply_time = refund_info.get("apply_time", "")
        estimated_process_time = refund_info.get("estimated_process_time", "")
        process_result = refund_info.get("process_result")
        
        if status == "处理中":
            return (f"您的退款申请 {refund_id}（订单号：{order_id}）正在处理中，"
                    f"申请时间：{apply_time}，预计处理完成时间：{estimated_process_time}。"
                    f"请您耐心等待，处理结果将通过短信通知您。")
        
        elif status == "已批准":
            refund_amount = refund_info.get("refund_amount", "0.00")
            return (f"您的退款申请 {refund_id}（订单号：{order_id}）已批准，"
                    f"退款金额：{refund_amount}元，款项将在3-5个工作日内原路退回到您的支付账户。"
                    f"如有问题请联系客服。")
        
        elif status == "已拒绝":
            return (f"您的退款申请 {refund_id}（订单号：{order_id}）已被拒绝，"
                    f"拒绝原因：{process_result or '请联系客服了解详情'}。"
                    f"如有疑问请联系客服。")
        
        else:
            return f"您的退款申请 {refund_id} 当前状态为：{status}，如需了解更多信息请联系客服。"

# 创建全局退款申请工具实例
refund_request_tool = RefundRequestTool()