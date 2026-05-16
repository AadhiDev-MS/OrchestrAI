import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..memory.database import get_session
from ..rag.ingestion import get_ingestion_service

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    """
    Upload a PDF and trigger the ingestion pipeline.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    try:
        # Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger ingestion
        ingestion_service = await get_ingestion_service(db)
        doc_id = await ingestion_service.ingest_pdf(file_path, file.filename)

        return {
            "message": "File uploaded and ingested successfully",
            "document_id": doc_id,
            "filename": file.filename
        }
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"INGESTION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.get("/status/{doc_id}")
async def get_ingestion_status(doc_id: str):
    # This would be more relevant with ARQ workers
    return {"status": "completed", "document_id": doc_id}
