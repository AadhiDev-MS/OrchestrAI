import uuid
import hashlib
from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .parser import pdf_parser
from .embeddings import embedding_service
from ..memory.models import Document, ParentChunk, ChildChunk

class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_pdf(self, file_path: str, filename: str) -> str:
        # 1. Parse PDF
        raw_text = await pdf_parser.parse_pdf(file_path)
        content_hash = hashlib.sha256(raw_text.encode()).hexdigest()

        # 2. Check if document already exists
        existing_doc = await self.db.execute(
            select(Document).where(Document.content_hash == content_hash)
        )
        doc = existing_doc.scalar_one_or_none()
        
        # FOR TESTING/FIXING: If doc exists but only has 1 chunk, we re-ingest
        # In production, we might want a 'force' flag
        if doc:
            chunk_count = await self.db.execute(
                select(ChildChunk).join(ParentChunk).where(ParentChunk.document_id == doc.id)
            )
            if len(chunk_count.all()) > 5: # If it has substantial chunks, skip
                return str(doc.id)
            else:
                # Delete old broken records
                await self.db.execute(delete(Document).where(Document.id == doc.id))
                await self.db.flush()

        # 3. Create Document
        doc = Document(
            filename=filename,
            content_hash=content_hash,
            metadata_json={"source": file_path, "type": "pdf"}
        )
        self.db.add(doc)
        await self.db.flush() 

        # 4. Split into Parent Chunks
        sections = pdf_parser.split_into_sections(raw_text)
        
        for i, section in enumerate(sections):
            if not section["content"].strip():
                continue

            parent = ParentChunk(
                document_id=doc.id,
                content=section["content"],
                header_path=section["header"],
                chunk_index=i
            )
            self.db.add(parent)
            await self.db.flush()

            # 5. Split into Child Chunks
            child_chunks_texts = self._create_child_chunks(section["content"])
            
            if not child_chunks_texts:
                continue

            # 6. Embed and Save
            embeddings = await embedding_service.embed_texts(child_chunks_texts)

            for k, (text, vector) in enumerate(zip(child_chunks_texts, embeddings)):
                child = ChildChunk(
                    parent_id=parent.id,
                    content=text,
                    embedding=vector,
                    chunk_index=k
                )
                self.db.add(child)

        await self.db.commit()
        return str(doc.id)

    def _create_child_chunks(self, text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
        chunks = []
        if not text:
            return chunks
            
        # Split by characters with overlap
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk) > 100: # Avoid tiny chunks at the end
                chunks.append(chunk)
        return chunks

async def get_ingestion_service(db: AsyncSession):
    return IngestionService(db)
