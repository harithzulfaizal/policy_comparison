import os
import aiofiles
import json_repair
import asyncio
from typing import Any, Dict
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, UploadFile, File

from app.logger import logger
from app.core.extract_sections import extract_sections
from app.core.match_sections import match_document_sections
from app.core.compare_sections import compare_sections

class CompareSections(BaseModel):
    session_id: str
    updated_sections: Dict


router = APIRouter()

@router.post("/edit_sections")
async def edit_sections(
    input: CompareSections
    ) -> Any:
    
    session_id = input.session_id
    updated_sections = input.updated_sections
    
    tasks = []
    for filename, properties in updated_sections.items():
        task = asyncio.create_task(extract_sections(
                session_id=session_id,
                filename=filename,
                starting_page=properties['page_num'],
                content=properties['content']
            )
        )

        tasks.append(task)
    
    both_sections = await asyncio.gather(*tasks)
    # both_sections = [json_repair.loads(s) for s in both_sections]

    sections_A, sections_B = both_sections[0], both_sections[1]

    sections_properties = await match_document_sections(sections_A=sections_A, sections_B=sections_B)
    sections_comparison = await compare_sections(
        sections_info=sections_properties['sections_info'],
        sections_A=sections_properties['sections_A'],
        sections_B=sections_properties['sections_B']
    )

    return sections_comparison
    
    
