import os
import json
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, TypedDict
import uuid
from datetime import datetime

from src.core.config import Config
from src.utils.logger import app_logger
from src.services.model_manager import model_manager
from src.services.plugin_manager import plugin_manager


class State(TypedDict):
    """定义状态图的状态结构"""
    messages: Annotated[list, add_messages]
    current_user: str
    session_id: str
    tools_available: bool


class ChatService:
    """聊天服务类，集成LangChain和LangGraph"""
    
    def __init__(self):
        """初始化聊天服务"""
        self.config = Config()
        self.app = self._build_state_graph()
        self.sessions = {}  # 存储会话状态
        app_logger.info("聊天服务初始化完成")
    
    def _build_state_graph(self) -> StateGraph:
        """构建状态图工作流"""
        # 创建状态图
        workflow = StateGraph(State)
        
        # 添加节点
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)
        
        # 设置入口点
        workflow.set_entry_point("agent")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        # 添加从工具节点回到代理节点的边
        workflow.add_edge("tools", "agent")
        
        # 编译图
        app = workflow.compile()
        
        app_logger.info("状态图工作流构建完成")
        return app
    
    def _should_continue(self, state: State) -> str:
        """决定是否继续调用工具"""
        last_message = state["messages"][-1] if state["messages"] else None
        
        # 如果最后一条消息是AI消息且包含工具调用，则继续
        if (last_message and 
            hasattr(last_message, 'additional_kwargs') and 
            last_message.additional_kwargs.get('tool_calls')):
            return "continue"
        
        # 否则结束
        return "end"
    
    def _call_model(self, state: State) -> Dict[str, Any]:
        """调用模型生成响应"""
        try:
            # 获取当前模型
            llm = model_manager.get_current_model()
            
            # 获取所有插件工具
            plugins = plugin_manager.get_all_plugins()
            tools = []
            for plugin_name, plugin_tools in plugins.items():
                tools.extend(plugin_tools)
            
            # 如果有工具，将工具绑定到模型
            if tools:
                tool_functions = [tool["function"] for tool in tools]
                llm_with_tools = llm.bind_tools(tool_functions)
            else:
                llm_with_tools = llm
            
            # 准备消息
            messages = state["messages"]
            
            # 调用模型
            response = llm_with_tools.invoke(messages)
            
            return {"messages": [response]}
        except Exception as e:
            app_logger.error(f"调用模型时出错: {str(e)}")
            error_message = AIMessage(content=f"抱歉，处理您的请求时出现错误: {str(e)}")
            return {"messages": [error_message]}
    
    def _call_tools(self, state: State) -> Dict[str, Any]:
        """执行工具调用"""
        try:
            # 获取最后一条消息
            last_message = state["messages"][-1]
            
            # 检查是否有工具调用
            if not (hasattr(last_message, 'additional_kwargs') and 
                    last_message.additional_kwargs.get('tool_calls')):
                return {"messages": []}
            
            tool_calls = last_message.additional_kwargs.get('tool_calls', [])
            tool_results = []
            
            # 执行每个工具调用
            for tool_call in tool_calls:
                function_name = tool_call.get('function', {}).get('name')
                function_args = json.loads(tool_call.get('function', {}).get('arguments', '{}'))
                
                try:
                    # 获取工具函数
                    tool_function = plugin_manager.get_plugin_function(function_name)
                    
                    if tool_function:
                        # 执行工具函数
                        result = tool_function(**function_args)
                        tool_results.append({
                            "tool_call_id": tool_call.get('id'),
                            "output": str(result)
                        })
                        app_logger.info(f"执行工具 {function_name} 成功")
                    else:
                        # 工具不存在
                        tool_results.append({
                            "tool_call_id": tool_call.get('id'),
                            "output": f"错误: 工具 {function_name} 不存在"
                        })
                        app_logger.warning(f"工具 {function_name} 不存在")
                except Exception as e:
                    # 工具执行出错
                    tool_results.append({
                        "tool_call_id": tool_call.get('id'),
                        "output": f"执行工具 {function_name} 时出错: {str(e)}"
                    })
                    app_logger.error(f"执行工具 {function_name} 时出错: {str(e)}")
            
            # 创建工具响应消息
            if tool_results:
                tool_message = AIMessage(
                    content="",
                    additional_kwargs={"tool_calls": tool_calls},
                    tool_calls=tool_results
                )
                return {"messages": [tool_message]}
            
            return {"messages": []}
        except Exception as e:
            app_logger.error(f"调用工具时出错: {str(e)}")
            error_message = AIMessage(content=f"执行工具时出现错误: {str(e)}")
            return {"messages": [error_message]}
    
    def _get_or_create_session(self, user_id: str, session_id: Optional[str] = None) -> str:
        """获取或创建会话"""
        if session_id and session_id in self.sessions:
            return session_id
        
        # 创建新会话
        new_session_id = str(uuid.uuid4())
        self.sessions[new_session_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        
        return new_session_id
    
    def process_input(self, user_id: str, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """处理用户输入并生成响应"""
        try:
            # 获取或创建会话
            session_id = self._get_or_create_session(user_id, session_id)
            
            # 添加用户消息到会话
            user_message = HumanMessage(content=message)
            
            # 准备状态
            state = {
                "messages": [user_message],
                "current_user": user_id,
                "session_id": session_id,
                "tools_available": True
            }
            
            # 调用状态图
            config = RunnableConfig(configurable={"thread_id": session_id})
            result = self.app.invoke(state, config=config)
            
            # 获取AI响应
            ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
            
            if not ai_messages:
                return {
                    "response": "抱歉，我无法生成响应。",
                    "session_id": session_id,
                    "status": "error"
                }
            
            # 获取最后一条AI消息
            last_ai_message = ai_messages[-1]
            response_content = last_ai_message.content if hasattr(last_ai_message, 'content') else str(last_ai_message)
            
            # 更新会话消息
            session = self.sessions[session_id]
            session["messages"].extend([user_message, last_ai_message])
            session["last_activity"] = datetime.now().isoformat()
            
            return {
                "response": response_content,
                "session_id": session_id,
                "status": "success",
                "tool_calls": last_ai_message.additional_kwargs.get('tool_calls') if hasattr(last_ai_message, 'additional_kwargs') else None
            }
        except Exception as e:
            app_logger.error(f"处理用户输入时出错: {str(e)}")
            return {
                "response": f"处理您的请求时出现错误: {str(e)}",
                "session_id": session_id if 'session_id' in locals() else None,
                "status": "error"
            }
    
    def get_session_history(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """获取会话历史"""
        try:
            if session_id not in self.sessions:
                return {
                    "error": "会话不存在",
                    "status": "error"
                }
            
            session = self.sessions[session_id]
            
            # 验证用户权限
            if session["user_id"] != user_id:
                return {
                    "error": "无权访问此会话",
                    "status": "error"
                }
            
            # 格式化消息历史
            formatted_messages = []
            for message in session["messages"]:
                if isinstance(message, HumanMessage):
                    formatted_messages.append({
                        "role": "user",
                        "content": message.content,
                        "timestamp": getattr(message, 'timestamp', None)
                    })
                elif isinstance(message, AIMessage):
                    formatted_messages.append({
                        "role": "assistant",
                        "content": message.content,
                        "timestamp": getattr(message, 'timestamp', None),
                        "tool_calls": message.additional_kwargs.get('tool_calls') if hasattr(message, 'additional_kwargs') else None
                    })
            
            return {
                "session_id": session_id,
                "user_id": session["user_id"],
                "created_at": session["created_at"],
                "last_activity": session.get("last_activity"),
                "messages": formatted_messages,
                "status": "success"
            }
        except Exception as e:
            app_logger.error(f"获取会话历史时出错: {str(e)}")
            return {
                "error": f"获取会话历史时出错: {str(e)}",
                "status": "error"
            }
    
    def delete_session(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """删除会话"""
        try:
            if session_id not in self.sessions:
                return {
                    "error": "会话不存在",
                    "status": "error"
                }
            
            session = self.sessions[session_id]
            
            # 验证用户权限
            if session["user_id"] != user_id:
                return {
                    "error": "无权删除此会话",
                    "status": "error"
                }
            
            # 删除会话
            del self.sessions[session_id]
            
            return {
                "message": "会话已删除",
                "status": "success"
            }
        except Exception as e:
            app_logger.error(f"删除会话时出错: {str(e)}")
            return {
                "error": f"删除会话时出错: {str(e)}",
                "status": "error"
            }
    
    def get_user_sessions(self, user_id: str) -> Dict[str, Any]:
        """获取用户的所有会话"""
        try:
            user_sessions = []
            for session_id, session in self.sessions.items():
                if session["user_id"] == user_id:
                    user_sessions.append({
                        "session_id": session_id,
                        "created_at": session["created_at"],
                        "last_activity": session.get("last_activity"),
                        "message_count": len(session["messages"])
                    })
            
            return {
                "user_id": user_id,
                "sessions": user_sessions,
                "status": "success"
            }
        except Exception as e:
            app_logger.error(f"获取用户会话时出错: {str(e)}")
            return {
                "error": f"获取用户会话时出错: {str(e)}",
                "status": "error"
            }
    
    def update_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """更新模型配置"""
        try:
            # 使用模型管理器更新模型
            result = model_manager.update_model(model_config)
            
            if result["success"]:
                # 重新构建状态图以使用新模型
                self.app = self._build_state_graph()
                app_logger.info("模型已更新，状态图已重新构建")
            
            return result
        except Exception as e:
            app_logger.error(f"更新模型时出错: {str(e)}")
            return {
                "success": False,
                "message": f"更新模型时出错: {str(e)}"
            }
    
    def reload_model_from_env(self) -> Dict[str, Any]:
        """从环境变量重新加载模型配置"""
        try:
            # 使用模型管理器从环境变量重新加载
            result = model_manager.reload_from_env()
            
            if result["success"]:
                # 重新构建状态图以使用新模型
                self.app = self._build_state_graph()
                app_logger.info("从环境变量重新加载模型成功，状态图已重新构建")
            
            return result
        except Exception as e:
            app_logger.error(f"从环境变量重新加载模型时出错: {str(e)}")
            return {
                "success": False,
                "message": f"从环境变量重新加载模型时出错: {str(e)}"
            }
    
    def reload_plugins(self) -> Dict[str, Any]:
        """重新加载所有插件"""
        try:
            # 使用插件管理器重新加载插件
            result = plugin_manager.reload_all_plugins()
            
            if result["success"]:
                # 重新构建状态图以使用新插件
                self.app = self._build_state_graph()
                app_logger.info("插件已重新加载，状态图已重新构建")
            
            return result
        except Exception as e:
            app_logger.error(f"重新加载插件时出错: {str(e)}")
            return {
                "success": False,
                "message": f"重新加载插件时出错: {str(e)}"
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        try:
            # 获取模型状态
            model_status = model_manager.get_current_model_info()
            
            # 获取插件状态
            plugin_status = plugin_manager.get_plugin_status()
            
            # 获取会话统计
            session_count = len(self.sessions)
            user_sessions = {}
            for session_id, session in self.sessions.items():
                user_id = session["user_id"]
                if user_id not in user_sessions:
                    user_sessions[user_id] = 0
                user_sessions[user_id] += 1
            
            return {
                "model": model_status,
                "plugins": plugin_status,
                "sessions": {
                    "total_sessions": session_count,
                    "unique_users": len(user_sessions),
                    "sessions_per_user": user_sessions
                },
                "status": "healthy"
            }
        except Exception as e:
            app_logger.error(f"获取服务状态时出错: {str(e)}")
            return {
                "error": f"获取服务状态时出错: {str(e)}",
                "status": "unhealthy"
            }