import os
import re
from typing import List, Dict, Any
from pypdf import PdfReader

class PDFParserService:
    def __init__(self):
        pass

    async def parse_pdf(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n\n"
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise e

    def split_into_sections(self, text: str, max_section_size: int = 5000) -> List[Dict[str, str]]:
        """
        Splits text into sections using a more robust regex for academic headers.
        """
        # Matches: "1 Introduction", "2.1 Methods", "Abstract", "References"
        header_pattern = re.compile(r'^(\d+(\.\d+)*\s+[A-Z][a-z]+|[A-Z][a-z]+)$', re.MULTILINE)
        
        sections = []
        lines = text.split('\n')
        current_header = "Abstract/Header"
        current_content = []

        for line in lines:
            line_strip = line.strip()
            # If line looks like a header (short and matches pattern)
            if header_pattern.match(line_strip) and len(line_strip) < 60:
                if current_content:
                    sections.append({
                        "header": current_header,
                        "content": "\n".join(current_content).strip()
                    })
                current_header = line_strip
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            sections.append({
                "header": current_header,
                "content": "\n".join(current_content).strip()
            })
            
        # If no sections were found (pattern missed everything), fallback to size-based
        if len(sections) <= 1:
            sections = []
            paragraphs = text.split('\n\n')
            current_content = []
            curr_size = 0
            for p in paragraphs:
                if curr_size + len(p) > max_section_size:
                    sections.append({"header": "Section", "content": "\n\n".join(current_content)})
                    current_content = [p]
                    curr_size = len(p)
                else:
                    current_content.append(p)
                    curr_size += len(p)
            if current_content:
                sections.append({"header": "Section", "content": "\n\n".join(current_content)})

        return sections

# Singleton instance
pdf_parser = PDFParserService()
