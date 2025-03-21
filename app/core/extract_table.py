import os
import asyncio
from typing import List, Dict
from pydantic import BaseModel

import base64
import pymupdf
import json_repair

from app.core.prompts import IS_TOC_PROMPT
from app.models.llm import gemini_2_flash

class Sections(BaseModel):
    sections: List[str]

class TOC(BaseModel):
    page_num: int
    is_toc: bool
    content: Sections

async def pdf_to_base64(pdf_bytes: bytes) -> list[str]:
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        base64_images = []

        for page_num in range(doc.page_count):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))

            img_bytes = pix.tobytes("jpeg")
            base64_img = base64.b64encode(img_bytes).decode("utf-8")
            base64_images.append(f"data:image/jpeg;base64,{base64_img}")

        doc.close()
        return base64_images
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []
    
async def extract_table(
        session_id: str,
        pdf_bytes: bytes,
    ) -> TOC:
        
        pages = await pdf_to_base64(pdf_bytes)
        tasks = []

        for page_num, page in enumerate(pages, start=1):
            task = asyncio.create_task(
                gemini_2_flash.aget_completion(
                    prompt=IS_TOC_PROMPT.format(page_num=page_num),
                    img_url=page,
                    response_format=TOC
                ))
            tasks.append(task)

        toc_found = []
        for future in asyncio.as_completed(tasks):
            result = await future
            result = json_repair.loads(result)

            if result['is_toc']:
                toc_found.append(result)

                for task in tasks:
                    if not task.done():
                        task.cancel()
                break 

        return toc_found[0]

             


