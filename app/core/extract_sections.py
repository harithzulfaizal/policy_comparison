import os
import asyncio
import aiofiles
from typing import List, Dict
from pydantic import BaseModel

import base64
import pymupdf4llm
import json_repair

from app.config import ROOT_DIR
from app.core.prompts import EXTRACT_SECTIONS_PROMPT
from app.models.llm import model

async def get_pdf_markdown(
        session_id: str,
        filename: str
    ):

    file_path = f"{ROOT_DIR}/tmp/{session_id}/{filename}"
    doc = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    return doc
    
async def extract_table(
        session_id: str,
        pdf_bytes: bytes,
    ):

    # async with aiofiles.open(pdf_filename, "rb") as f:

        
    pass

             


