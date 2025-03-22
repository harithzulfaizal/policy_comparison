import os
import aiofiles
import json
import asyncio
from typing import Any, Dict
from fastapi import HTTPException, APIRouter, UploadFile, File

from app.config import ROOT_DIR
from app.logger import logger
from app.core.extract_table import extract_table, TOC


router = APIRouter()

@router.post("/upload_documents")
async def upload_documents(
    session_id: str,
    file_A: UploadFile = File(...),
    file_B: UploadFile = File(...),
    ) -> Dict:

    tasks = []

    for file in [file_A, file_B]:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
        pdf_bytes = await file.read()
        folder_path = f"{ROOT_DIR}/tmp/{session_id}"
        os.makedirs(folder_path, exist_ok=True)

        file_path = f"{folder_path}/{file.filename}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(pdf_bytes)
        logger.info(f"File {file.filename} saved locally.")

        tasks.append(asyncio.create_task(extract_table(session_id=session_id, pdf_bytes=pdf_bytes)))

    results = await asyncio.gather(*tasks)

    return {
        file_A.filename: results[0],
        file_B.filename: results[1]
    }