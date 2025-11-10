from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.chat_service import ChatService
from src.utils.logger import app_logger

# 创建路由器
router = APIRouter()

# 创建聊天服务实例
chat_service = ChatService()

# 请求模型
class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class SessionHistoryRequest(BaseModel):
    user_id: str
    session_id: str

class DeleteSessionRequest(BaseModel):
    user_id: str
    session_id: str

class ModelUpdateRequest(BaseModel):
    model_config_data: Dict[str, Any]

# 根路径
@router.get("/")
async def root():
    return {"message": "智能客服聊天服务"}

# 健康检查接口
@router.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 获取服务状态
        status = chat_service.get_service_status()
        
        # 检查服务是否健康
        if status.get("status") == "healthy":
            return {
                "status": "healthy",
                "message": "服务运行正常",
                "details": status
            }
        else:
            return {
                "status": "unhealthy",
                "message": "服务存在问题",
                "details": status
            }
    except Exception as e:
        app_logger.error(f"健康检查时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")

# 聊天接口
@router.post("/chat")
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        result = chat_service.process_input(
            user_id=request.user_id,
            message=request.message,
            session_id=request.session_id
        )
        
        if result["status"] == "success":
            return {
                "success": True,
                "response": result["response"],
                "session_id": result["session_id"],
                "tool_calls": result.get("tool_calls")
            }
        else:
            return {
                "success": False,
                "error": result.get("response", "处理请求时出现未知错误")
            }
    except Exception as e:
        app_logger.error(f"处理聊天请求时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理聊天请求时出错: {str(e)}")

# 获取会话历史
@router.post("/session/history")
async def get_session_history(request: SessionHistoryRequest):
    """获取会话历史"""
    try:
        result = chat_service.get_session_history(
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        if result["status"] == "success":
            return {
                "success": True,
                "session": result
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "获取会话历史失败")
            }
    except Exception as e:
        app_logger.error(f"获取会话历史时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取会话历史时出错: {str(e)}")

# 删除会话
@router.delete("/session")
async def delete_session(request: DeleteSessionRequest):
    """删除会话"""
    try:
        result = chat_service.delete_session(
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        if result["status"] == "success":
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "删除会话失败")
            }
    except Exception as e:
        app_logger.error(f"删除会话时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除会话时出错: {str(e)}")

# 获取用户的所有会话
@router.get("/session/list/{user_id}")
async def get_user_sessions(user_id: str):
    """获取用户的所有会话"""
    try:
        result = chat_service.get_user_sessions(user_id)
        
        if result["status"] == "success":
            return {
                "success": True,
                "sessions": result["sessions"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "获取用户会话失败")
            }
    except Exception as e:
        app_logger.error(f"获取用户会话时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取用户会话时出错: {str(e)}")

# 热更新相关接口

# 更新模型配置
@router.post("/admin/model/update")
async def update_model(request: ModelUpdateRequest):
    """更新模型配置"""
    try:
        result = chat_service.update_model(request.model_config_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "model_status": result.get("model_status")
            }
        else:
            return {
                "success": False,
                "error": result["message"]
            }
    except Exception as e:
        app_logger.error(f"更新模型配置时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新模型配置时出错: {str(e)}")

# 从环境变量重新加载模型配置
@router.post("/admin/model/reload")
async def reload_model_from_env():
    """从环境变量重新加载模型配置"""
    try:
        result = chat_service.reload_model_from_env()
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "model_status": result.get("model_status")
            }
        else:
            return {
                "success": False,
                "error": result["message"]
            }
    except Exception as e:
        app_logger.error(f"从环境变量重新加载模型配置时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"从环境变量重新加载模型配置时出错: {str(e)}")

# 重新加载所有插件
@router.post("/admin/plugins/reload")
async def reload_plugins():
    """重新加载所有插件"""
    try:
        result = chat_service.reload_plugins()
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "plugin_status": result.get("plugin_status")
            }
        else:
            return {
                "success": False,
                "error": result["message"],
                "failed_plugins": result.get("failed_plugins", [])
            }
    except Exception as e:
        app_logger.error(f"重新加载插件时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"重新加载插件时出错: {str(e)}")

# 获取服务状态
@router.get("/admin/status")
async def get_service_status():
    """获取服务状态"""
    try:
        status = chat_service.get_service_status()
        
        return {
            "success": True,
            "status": status
        }
    except Exception as e:
        app_logger.error(f"获取服务状态时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取服务状态时出错: {str(e)}")