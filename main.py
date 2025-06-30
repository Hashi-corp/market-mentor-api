from fastapi import FastAPI
from app.routes import stock, news, llm

app = FastAPI(title="Market Mentor API",
             description="API for Indian stock market research and analysis",
             version="1.0.0")

app.include_router(stock.router, prefix="/api", tags=["Stocks"])
app.include_router(news.router, prefix="/api", tags=["News"])
app.include_router(llm.router, prefix="/api", tags=["LLM"])

@app.get("/")
async def root():
    return {"message": "Welcome to Market Mentor API for Indian stock market research"}
