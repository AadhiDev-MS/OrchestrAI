import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255))
    content_hash: Mapped[str] = mapped_column(String(64), unique=True)  # To avoid duplicates
    metadata_json: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    parents: Mapped[List["ParentChunk"]] = relationship("ParentChunk", back_populates="document", cascade="all, delete-orphan")

class ParentChunk(Base):
    __tablename__ = "parent_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    content: Mapped[str] = mapped_column(Text)
    header_path: Mapped[str] = mapped_column(Text)  # e.g., "Introduction > Methodology"
    chunk_index: Mapped[int] = mapped_column()

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="parents")
    children: Mapped[List["ChildChunk"]] = relationship("ChildChunk", back_populates="parent", cascade="all, delete-orphan")

class ChildChunk(Base):
    __tablename__ = "child_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("parent_chunks.id"))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(768))  # gemini-embedding-2 is reduced to 768 dims
    chunk_index: Mapped[int] = mapped_column()

    # Relationships
    parent: Mapped["ParentChunk"] = relationship("ParentChunk", back_populates="children")

# Index for vector similarity search
Index(
    "idx_child_chunks_embedding", 
    ChildChunk.embedding, 
    postgresql_using="hnsw", 
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"}
)
