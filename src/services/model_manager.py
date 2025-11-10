import os
import importlib
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from src.core.config import config
from src.utils.logger import app_logger

class ModelManager:
    """模型管理器，负责模型的热更新"""
    
    def __init__(self):
        self.current_model = None
        self.current_model_name = config.OPENAI_MODEL
        self.current_api_key = config.OPENAI_API_KEY
        self.current_api_base = config.OPENAI_API_BASE
        self._init_model()
    
    def _init_model(self):
        """初始化模型"""
        try:
            self.current_model = ChatOpenAI(
                model=self.current_model_name,
                openai_api_key=self.current_api_key,
                openai_api_base=self.current_api_base,
                temperature=0.7
            )
            app_logger.info(f"模型初始化成功: {self.current_model_name}")
        except Exception as e:
            app_logger.error(f"模型初始化失败: {str(e)}")
            raise
    
    def get_current_model(self):
        """获取当前模型"""
        return self.current_model
    
    def get_current_model_info(self) -> Dict[str, str]:
        """获取当前模型信息"""
        return {
            "model_name": self.current_model_name,
            "api_base": self.current_api_base,
            "status": "active"
        }
    
    def update_model(self, model_name: Optional[str] = None, 
                    api_key: Optional[str] = None, 
                    api_base: Optional[str] = None) -> Dict[str, Any]:
        """
        更新模型配置
        
        Args:
            model_name: 新的模型名称
            api_key: 新的API密钥
            api_base: 新的API基础URL
            
        Returns:
            包含更新结果的字典
        """
        try:
            # 保存旧配置以便回滚
            old_model_name = self.current_model_name
            old_api_key = self.current_api_key
            old_api_base = self.current_api_base
            
            # 更新配置
            if model_name:
                self.current_model_name = model_name
            if api_key:
                self.current_api_key = api_key
            if api_base:
                self.current_api_base = api_base
            
            # 初始化新模型
            self._init_model()
            
            app_logger.info(f"模型更新成功: {self.current_model_name}")
            
            return {
                "success": True,
                "message": f"模型已成功更新为: {self.current_model_name}",
                "old_model": old_model_name,
                "new_model": self.current_model_name
            }
        except Exception as e:
            # 回滚到旧配置
            self.current_model_name = old_model_name
            self.current_api_key = old_api_key
            self.current_api_base = old_api_base
            
            app_logger.error(f"模型更新失败，已回滚到旧配置: {str(e)}")
            
            return {
                "success": False,
                "message": f"模型更新失败: {str(e)}",
                "current_model": self.current_model_name
            }
    
    def reload_from_env(self) -> Dict[str, Any]:
        """从环境变量重新加载模型配置"""
        try:
            # 从环境变量读取新配置
            new_model_name = os.getenv("OPENAI_MODEL", self.current_model_name)
            new_api_key = os.getenv("OPENAI_API_KEY", self.current_api_key)
            new_api_base = os.getenv("OPENAI_API_BASE", self.current_api_base)
            
            # 检查是否有变化
            if (new_model_name == self.current_model_name and 
                new_api_key == self.current_api_key and 
                new_api_base == self.current_api_base):
                return {
                    "success": True,
                    "message": "模型配置无变化，无需更新"
                }
            
            # 更新模型
            return self.update_model(new_model_name, new_api_key, new_api_base)
        except Exception as e:
            app_logger.error(f"从环境变量重新加载模型配置失败: {str(e)}")
            return {
                "success": False,
                "message": f"从环境变量重新加载模型配置失败: {str(e)}"
            }

# 创建全局模型管理器实例
model_manager = ModelManager()