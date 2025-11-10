import os
import importlib
import inspect
from typing import Dict, Any, List, Callable, Optional
from src.utils.logger import app_logger

class PluginManager:
    """插件管理器，负责插件的热重载"""
    
    def __init__(self):
        self.plugins = {}
        self.plugin_modules = {}
        self.plugin_functions = {}
        self._load_plugins()
    
    def _load_plugins(self):
        """加载所有插件"""
        try:
            plugins_dir = os.path.join(os.path.dirname(__file__), "..", "tools")
            
            # 确保插件目录存在
            if not os.path.exists(plugins_dir):
                app_logger.warning(f"插件目录不存在: {plugins_dir}")
                return
            
            # 遍历插件目录中的所有Python文件
            for filename in os.listdir(plugins_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    plugin_name = filename[:-3]  # 移除.py扩展名
                    self._load_plugin(plugin_name)
            
            app_logger.info(f"已加载 {len(self.plugins)} 个插件")
        except Exception as e:
            app_logger.error(f"加载插件时出错: {str(e)}")
    
    def _load_plugin(self, plugin_name: str):
        """加载单个插件"""
        try:
            # 构建模块路径
            module_path = f"src.tools.{plugin_name}"
            
            # 导入模块
            module = importlib.import_module(module_path)
            
            # 保存模块引用以便重载
            self.plugin_modules[plugin_name] = module
            
            # 查找插件中的工具函数
            tools = []
            for name, obj in inspect.getmembers(module):
                if (inspect.isfunction(obj) and 
                    not name.startswith("_") and 
                    hasattr(obj, "__doc__") and 
                    obj.__doc__):
                    
                    # 保存函数引用
                    self.plugin_functions[f"{plugin_name}.{name}"] = obj
                    tools.append({
                        "name": f"{plugin_name}.{name}",
                        "description": obj.__doc__,
                        "function": obj
                    })
            
            if tools:
                self.plugins[plugin_name] = tools
                app_logger.info(f"已加载插件: {plugin_name}, 包含 {len(tools)} 个工具")
            else:
                app_logger.warning(f"插件 {plugin_name} 中没有找到有效的工具函数")
        except Exception as e:
            app_logger.error(f"加载插件 {plugin_name} 时出错: {str(e)}")
    
    def get_plugin(self, plugin_name: str) -> Optional[List[Dict[str, Any]]]:
        """获取指定插件"""
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取所有插件"""
        return self.plugins
    
    def get_plugin_function(self, function_name: str) -> Optional[Callable]:
        """获取指定的插件函数"""
        return self.plugin_functions.get(function_name)
    
    def reload_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """重新加载指定插件"""
        try:
            if plugin_name not in self.plugins:
                return {
                    "success": False,
                    "message": f"插件 {plugin_name} 不存在"
                }
            
            # 重新加载模块
            module_path = f"src.tools.{plugin_name}"
            if module_path in self.plugin_modules:
                module = importlib.reload(self.plugin_modules[module_path])
            else:
                module = importlib.import_module(module_path)
                self.plugin_modules[module_path] = module
            
            # 清除旧的插件函数
            old_function_names = [
                name for name in self.plugin_functions.keys() 
                if name.startswith(f"{plugin_name}.")
            ]
            for name in old_function_names:
                del self.plugin_functions[name]
            
            # 重新加载插件函数
            tools = []
            for name, obj in inspect.getmembers(module):
                if (inspect.isfunction(obj) and 
                    not name.startswith("_") and 
                    hasattr(obj, "__doc__") and 
                    obj.__doc__):
                    
                    # 保存函数引用
                    self.plugin_functions[f"{plugin_name}.{name}"] = obj
                    tools.append({
                        "name": f"{plugin_name}.{name}",
                        "description": obj.__doc__,
                        "function": obj
                    })
            
            if tools:
                self.plugins[plugin_name] = tools
                app_logger.info(f"已重新加载插件: {plugin_name}, 包含 {len(tools)} 个工具")
                
                return {
                    "success": True,
                    "message": f"插件 {plugin_name} 已成功重新加载",
                    "tools_count": len(tools)
                }
            else:
                # 如果没有找到工具函数，移除插件
                del self.plugins[plugin_name]
                return {
                    "success": False,
                    "message": f"重新加载后，插件 {plugin_name} 中没有找到有效的工具函数，已移除"
                }
        except Exception as e:
            app_logger.error(f"重新加载插件 {plugin_name} 时出错: {str(e)}")
            return {
                "success": False,
                "message": f"重新加载插件 {plugin_name} 时出错: {str(e)}"
            }
    
    def reload_all_plugins(self) -> Dict[str, Any]:
        """重新加载所有插件"""
        try:
            plugin_names = list(self.plugins.keys())
            success_count = 0
            failed_plugins = []
            
            for plugin_name in plugin_names:
                result = self.reload_plugin(plugin_name)
                if result["success"]:
                    success_count += 1
                else:
                    failed_plugins.append({
                        "plugin": plugin_name,
                        "error": result["message"]
                    })
            
            app_logger.info(f"已重新加载 {success_count}/{len(plugin_names)} 个插件")
            
            return {
                "success": len(failed_plugins) == 0,
                "message": f"已重新加载 {success_count}/{len(plugin_names)} 个插件",
                "success_count": success_count,
                "total_count": len(plugin_names),
                "failed_plugins": failed_plugins
            }
        except Exception as e:
            app_logger.error(f"重新加载所有插件时出错: {str(e)}")
            return {
                "success": False,
                "message": f"重新加载所有插件时出错: {str(e)}"
            }
    
    def load_new_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """加载新插件"""
        try:
            if plugin_name in self.plugins:
                return {
                    "success": False,
                    "message": f"插件 {plugin_name} 已存在"
                }
            
            self._load_plugin(plugin_name)
            
            if plugin_name in self.plugins:
                tools_count = len(self.plugins[plugin_name])
                return {
                    "success": True,
                    "message": f"新插件 {plugin_name} 已成功加载，包含 {tools_count} 个工具",
                    "tools_count": tools_count
                }
            else:
                return {
                    "success": False,
                    "message": f"加载插件 {plugin_name} 失败，插件中没有找到有效的工具函数"
                }
        except Exception as e:
            app_logger.error(f"加载新插件 {plugin_name} 时出错: {str(e)}")
            return {
                "success": False,
                "message": f"加载新插件 {plugin_name} 时出错: {str(e)}"
            }
    
    def unload_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """卸载插件"""
        try:
            if plugin_name not in self.plugins:
                return {
                    "success": False,
                    "message": f"插件 {plugin_name} 不存在"
                }
            
            # 清除插件函数
            function_names = [
                name for name in self.plugin_functions.keys() 
                if name.startswith(f"{plugin_name}.")
            ]
            for name in function_names:
                del self.plugin_functions[name]
            
            # 移除插件
            tools_count = len(self.plugins[plugin_name])
            del self.plugins[plugin_name]
            
            app_logger.info(f"已卸载插件: {plugin_name}")
            
            return {
                "success": True,
                "message": f"插件 {plugin_name} 已成功卸载，移除了 {tools_count} 个工具",
                "tools_count": tools_count
            }
        except Exception as e:
            app_logger.error(f"卸载插件 {plugin_name} 时出错: {str(e)}")
            return {
                "success": False,
                "message": f"卸载插件 {plugin_name} 时出错: {str(e)}"
            }
    
    def get_plugin_status(self) -> Dict[str, Any]:
        """获取插件状态"""
        try:
            total_plugins = len(self.plugins)
            total_tools = sum(len(tools) for tools in self.plugins.values())
            
            plugin_details = {}
            for plugin_name, tools in self.plugins.items():
                plugin_details[plugin_name] = {
                    "tools_count": len(tools),
                    "tools": [tool["name"] for tool in tools]
                }
            
            return {
                "total_plugins": total_plugins,
                "total_tools": total_tools,
                "plugins": plugin_details
            }
        except Exception as e:
            app_logger.error(f"获取插件状态时出错: {str(e)}")
            return {
                "error": f"获取插件状态时出错: {str(e)}"
            }

# 创建全局插件管理器实例
plugin_manager = PluginManager()