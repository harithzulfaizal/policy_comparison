import os
import aiofiles
import json
import asyncio
from typing import Any, Dict
from fastapi import HTTPException, APIRouter, UploadFile, File

from app.logger import logger
from app.core.extract_table import extract_table, TOC


router = APIRouter()

@router.post("/edit_sections")
async def edit_sections(
    session_id: str,
    updated_sections: Dict
    ) -> Dict:

    pass