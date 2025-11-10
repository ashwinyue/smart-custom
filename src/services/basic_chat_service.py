from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from src.core.config import config

class BasicChatService:
    """基础对话服务类，实现LangChain基础链"""
    
    def __init__(self):
        # 初始化语言模型
        self.model = ChatOpenAI(
            model=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
            openai_api_base=config.OPENAI_API_BASE,
            temperature=0.7
        )
        
        # 初始化时间推断链
        self.time_inference_chain = self._create_time_inference_chain()
        
        # 初始化基础对话链
        self.basic_chat_chain = self._create_basic_chat_chain()
    
    def _create_time_inference_chain(self) -> RunnableParallel:
        """创建时间推断链"""
        # 时间推断提示模板
        time_template = """
        你是一个时间推断助手。根据当前日期和用户描述的时间相对表达，推断出具体的日期。
        
        当前日期: {current_date}
        用户描述: {time_expression}
        
        请推断出具体的日期，格式为YYYY-MM-DD。只返回日期，不要其他内容。
        """
        
        time_prompt = PromptTemplate(
            input_variables=["current_date", "time_expression"],
            template=time_template
        )
        
        # 创建时间推断链
        time_chain = time_prompt | self.model | StrOutputParser()
        
        return RunnableParallel({
            "current_date": lambda x: datetime.now().strftime("%Y-%m-%d"),
            "time_expression": lambda x: x["time_expression"],
            "inferred_date": time_chain
        })
    
    def _create_basic_chat_chain(self) -> RunnableParallel:
        """创建基础对话链"""
        # 基础对话提示模板
        chat_template = """
        你是一个智能客服助手，能够理解用户的问题并提供有用的回答。
        
        用户问题: {user_input}
        当前日期: {current_date}
        
        请提供友好、专业的回答。
        """
        
        chat_prompt = PromptTemplate(
            input_variables=["user_input", "current_date"],
            template=chat_template
        )
        
        # 创建基础对话链
        chat_chain = chat_prompt | self.model | StrOutputParser()
        
        return RunnableParallel({
            "current_date": lambda x: datetime.now().strftime("%Y-%m-%d"),
            "user_input": lambda x: x["user_input"],
            "response": chat_chain
        })
    
    def infer_time(self, time_expression: str) -> Dict[str, Any]:
        """
        推断时间表达式的具体日期
        
        Args:
            time_expression: 时间表达式，如"昨天"、"上周三"等
            
        Returns:
            包含推断结果的字典
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            result = self.time_inference_chain.invoke({
                "time_expression": time_expression,
                "current_date": current_date
            })
            return {
                "success": True,
                "time_expression": time_expression,
                "inferred_date": result["inferred_date"],
                "current_date": result["current_date"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time_expression": time_expression
            }
    
    def chat(self, user_input: str, conversation_history: Optional[list] = None) -> Dict[str, Any]:
        """
        基础对话功能
        
        Args:
            user_input: 用户输入
            conversation_history: 对话历史（可选）
            
        Returns:
            包含AI响应的字典
        """
        try:
            # 检查是否包含时间表达式
            time_expressions = ["昨天", "前天", "今天", "明天", "后天", "上周", "下周", "上个月", "下个月"]
            contains_time_expr = any(expr in user_input for expr in time_expressions)
            
            # 如果包含时间表达式，先进行时间推断
            time_info = {}
            if contains_time_expr:
                # 简单的时间表达式提取（实际应用中可以使用更复杂的NLP技术）
                for expr in time_expressions:
                    if expr in user_input:
                        time_result = self.infer_time(expr)
                        if time_result["success"]:
                            time_info = time_result
                            break
            
            # 运行基础对话链
            current_date = datetime.now().strftime("%Y-%m-%d")
            result = self.basic_chat_chain.invoke({
                "user_input": user_input,
                "current_date": current_date
            })
            
            # 构建响应
            response = result["response"]
            
            # 如果有时间推断信息，添加到响应中
            if time_info and time_info["success"]:
                response = f"{response}\n\n(时间推断: 您提到的'{time_info['time_expression']}'是指{time_info['inferred_date']})"
            
            return {
                "success": True,
                "response": response,
                "current_date": result["current_date"],
                "time_inference": time_info if time_info else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "抱歉，处理您的请求时出现了错误。"
            }

# 创建全局基础聊天服务实例
basic_chat_service = BasicChatService()