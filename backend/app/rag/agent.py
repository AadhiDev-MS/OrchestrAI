import os
import asyncio
from typing import List, Dict, Any
from google import genai
from google.genai import types

class ResearchAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-3-flash-preview" 

    async def synthesize_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Takes search results and generates a coherent, cited answer.
        """
        context_text = "\n\n".join([
            f"SOURCE: {c['header']}\nCONTENT: {c['child_content']}" 
            for c in context_chunks
        ])

        prompt = f"""
        You are OrchestrAI, an elite academic research assistant. 
        Your goal is to provide a cohesive, well-structured synthesis of the research data provided below.
        
        USER_QUERY: {query}
        
        CONTEXT:
        {context_text}
        
        INSTRUCTIONS:
        1.  **Format**: Do NOT just list bullet points. Write in structured paragraphs.
        2.  **Synthesis**: Combine information from different sources into a clear narrative.
        3.  **Tone**: Maintain a professional, objective, and technical tone.
        4.  **Citations**: Use [Header Name] at the end of sentences where relevant.
        5.  **Organization**: Use bold headers for key themes (e.g., **Key Findings**, **Methodology**, **Impact**).
        6.  **Constraint**: If the context doesn't have the info, explain what is missing.
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
