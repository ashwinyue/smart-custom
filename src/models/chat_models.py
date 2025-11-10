from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class TimeInference(BaseModel):
    """时间推断模型"""
    time_expression: str
    inferred_date: Optional[str] = None
    current_date: Optional[str] = None
    success: bool
    error: Optional[str] = None

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    success: bool
    error: Optional[str] = None
    time_inference: Optional[TimeInference] = None

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str