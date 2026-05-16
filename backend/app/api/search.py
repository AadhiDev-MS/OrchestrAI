from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..memory.database import get_session
from ..rag.retrieval import get_retriever_service
from ..rag.agent import research_agent

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
async def search_documents(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_session)
):
    """
    Search ingested documents and synthesize an answer.
    """
    retriever = await get_retriever_service(db)
    results = await retriever.search(q, top_k=top_k)
    
    # Generate AI Synthesis
    answer = "No results found to synthesize."
    if results:
        answer = await research_agent.synthesize_answer(q, results)
    
    return {
        "query": q,
        "answer": answer,
        "results": results
    }
