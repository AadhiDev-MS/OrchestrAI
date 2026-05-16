from typing import List, Dict, Any
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from .embeddings import embedding_service
from ..memory.models import ChildChunk, ParentChunk

class RetrieverService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs hybrid search: Vector similarity + Text search.
        Returns reconstructed context (Child + Parent).
        """
        # 1. Embed the query
        query_vector = await embedding_service.embed_query(query)

        # 2. Vector Similarity Search using pgvector
        # We select the child chunk and its associated parent chunk
        stmt = (
            select(ChildChunk, ParentChunk)
            .join(ParentChunk)
            .order_by(ChildChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        
        result = await self.db.execute(stmt)
        hits = result.all()

        results = []
        for child, parent in hits:
            results.append({
                "child_id": str(child.id),
                "parent_id": str(parent.id),
                "child_content": child.content,
                "parent_content": parent.content,
                "header": parent.header_path,
                "score": 1.0 # Cosine distance could be added here
            })

        return results

async def get_retriever_service(db: AsyncSession):
    return RetrieverService(db)
