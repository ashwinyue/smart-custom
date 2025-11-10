"""
工具基类

提供所有工具类的通用功能和接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.utils.logger import app_logger


class BaseTool(ABC):
    """工具基类，提供通用功能"""
    
    def __init__(self):
        """初始化工具"""
        self.logger = app_logger
    
    @abstractmethod
    def get_name(self) -> str:
        """获取工具名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取工具描述"""
        pass
    
    def log_info(self, message: str) -> None:
        """记录信息日志"""
        self.logger.info(message)
    
    def log_error(self, message: str) -> None:
        """记录错误日志"""
        self.logger.error(message)
    
    def handle_exception(self, e: Exception, context: str = "") -> Dict[str, Any]:
        """统一处理异常"""
        error_msg = f"{context}: {str(e)}" if context else str(e)
        self.log_error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }