from fastapi import APIRouter
from pydantic import BaseModel
from app.models.response_models import APIResponse
from app.services.llm_service import get_stock_analysis

router = APIRouter()

class LLMQueryRequest(BaseModel):
    symbol: str
    question: str

@router.post("/llm-query", response_model=APIResponse)
async def llm_query(request: LLMQueryRequest):
    """Query LLM for stock analysis and information"""
    # Get analysis from LLM service
    answer = get_stock_analysis(request.symbol, request.question)
    return APIResponse(success=True, data={"answer": answer})