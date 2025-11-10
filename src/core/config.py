from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class Config:
    """应用程序配置类"""
    
    # API配置
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # DashScope配置（已弃用）
    # DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # LangChain配置
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    
    @classmethod
    def validate(cls):
        """验证必要的配置项"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 环境变量未设置")
        return True

# 创建全局配置实例
config = Config()