from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, Chunk
from app.services.pdf_service import extract_text
from app.utils.text_cleaner import clean_text
from app.services.chunk_service import chunk_text
from app.schemas import ChunkResponse

router = APIRouter(tags=["Ingestion"])

@router.post("/ingest")
async def ingest_pdf(
    file: UploadFile = File(...),
    grade: int = Form(None),
    subject: str = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    try:
        raw_text = extract_text(file.file)
        cleaned_text = clean_text(raw_text)
        chunks_text = chunk_text(cleaned_text, max_words=200)
        
        # Save Source
        source = Source(
            file_name=file.filename,
            grade=grade,
            subject=subject
        )
        db.add(source)
        db.flush() # flush to get source id
        
        # Save Chunks
        db_chunks = []
        for text_chunk in chunks_text:
            chunk = Chunk(
                source_id=source.id,
                grade=grade,
                subject=subject,
                text=text_chunk
            )
            db.add(chunk)
            db_chunks.append(chunk)
            
        db.commit()
        
        return {
            "message": f"Successfully ingested {file.filename} into {len(db_chunks)} chunks.",
            "source_id": source.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
