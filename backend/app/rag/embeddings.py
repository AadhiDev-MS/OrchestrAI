import os
import asyncio
from typing import List
from google import genai
from google.genai import types

class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-embedding-2"

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of strings using Gemini embedding models."""
        loop = asyncio.get_event_loop()

        def _embed():
            result = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768)
            )
            return [e.values for e in result.embeddings]

        return await loop.run_in_executor(None, _embed)

    async def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        loop = asyncio.get_event_loop()

        def _embed():
            result = self.client.models.embed_content(
                model=self.model,
                contents=[text],
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY", output_dimensionality=768)
            )
            return result.embeddings[0].values

        return await loop.run_in_executor(None, _embed)

# Singleton instance
embedding_service = EmbeddingService()
