import os
import asyncio
from typing import List, Dict, Any
from google import genai
from google.genai import types

class ResearchAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-flash" 

    async def synthesize_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Takes search results and generates a coherent, cited answer.
        """
        context_text = "\n\n".join([
            f"SOURCE: {c['header']}\nCONTENT: {c['child_content']}" 
            for c in context_chunks
        ])

        prompt = f"""
        You are OrchestrAI, a high-level research assistant. 
        Your task is to answer the USER_QUERY using ONLY the provided CONTEXT. 
        If the answer isn't in the context, say you don't know.
        
        USER_QUERY: {query}
        
        CONTEXT:
        {context_text}
        
        INSTRUCTIONS:
        1. Be technical and precise.
        2. Cite sources using [Header Name].
        3. Use professional markdown formatting.
        4. Focus on 'the result' if that is what the user asked.
        """

        try:
            loop = asyncio.get_event_loop()
            
            def _generate():
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text

            return await loop.run_in_executor(None, _generate)
        except Exception as e:
            return f"Error synthesizing answer: {str(e)}"

# Singleton instance
research_agent = ResearchAgent()
