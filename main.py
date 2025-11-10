from fastapi import FastAPI
from src.core.config import config
from src.api.chat_routes import router as chat_router
from src.utils.logger import app_logger

# 创建FastAPI应用实例
app = FastAPI(
    title="Smart Custom API",
    description="基于FastAPI、LangChain和LangGraph的智能对话API",
    version="0.1.0"
)

# 注册路由
app.include_router(chat_router, tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    
    try:
        # 验证配置
        app_logger.info("正在验证配置...")
        config.validate()
        app_logger.info("配置验证成功")
        
        # 启动应用
        app_logger.info(f"正在启动应用，监听地址: {config.API_HOST}:{config.API_PORT}")
        uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
    except Exception as e:
        app_logger.error(f"启动应用时出错: {str(e)}")
        raise
