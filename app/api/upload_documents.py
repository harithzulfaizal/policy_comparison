import os
import aiofiles
import json
import asyncio
from typing import Any, Dict
from fastapi import HTTPException, APIRouter, UploadFile, File

from app.logger import logger
from app.core.extract_table import extract_table, TOC


router = APIRouter()

@router.post("/upload_documents")
async def upload_document(
    session_id: str,
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    ) -> Dict:

    tasks = []

    for file in [file_a, file_b]:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
        pdf_bytes = await file.read()

        tasks.append(asyncio.create_task(extract_table(session_id=session_id, pdf_bytes=pdf_bytes)))

    results = await asyncio.gather(*tasks)

    return {
        file_a.filename: results[0],
        file_b.filename: results[1]
    }