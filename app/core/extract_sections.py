import os
import re
import asyncio
import aiofiles
from typing import List, Dict
from pydantic import BaseModel

import base64
import pymupdf4llm
import json_repair

from app.config import ROOT_DIR
from app.logger import logger
from app.core.prompts import EXTRACT_SECTIONS_PROMPT
from app.models.llm import model

async def get_pdf_markdown(
        session_id: str,
        filename: str
    ) -> List:

    file_path = f"{ROOT_DIR}/tmp/{session_id}/{filename}"
    md_doc = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    return md_doc

def join_string_from_dict(sdict):
    string = ""
    for k, v in sdict.items():
        if type(v) == dict:
            v = join_string_from_dict(v)
        elif type(v) == list:
            v = " ".join(v)
        string += k + v
    return string

def parse_sections(sections_uncleaned, init_sections):
    sections_dict = {}
    added_sections = []

    for sections in sections_uncleaned:
        sections_exist = list(key.lower() for key in sections.keys())
        print(sections_exist)
        
        for section_title, content in sections.items():
            section_title = section_title.lower()
            print(section_title)

            if type(content) == dict:
                content = join_string_from_dict(content)

            if len(init_sections) >= 1:
                if section_title in init_sections[0].lower() or init_sections[0].lower() in section_title:
                    sections_dict[init_sections[0]] = content
                    added_sections.append(init_sections[0])
                    init_sections.remove(init_sections[0])
                elif section_title not in init_sections[0].lower() or init_sections[0].lower() in section_title:
                    sections_dict[added_sections[-1]] = sections_dict[added_sections[-1]] + content
            else:
                for s in init_sections:
                    if s.lower() in section_title or section_title in s.lower():
                        init_sections.remove(s)
            # else:
            #     for k, v in secs_.items():
            #         if v != "":
            #             sections_dict[added_sections[-1]] = sections_dict[added_sections[-1]] + v
                    
        print(f"added_sections ====== {added_sections}")
    return sections_dict


async def extract_sections(
        session_id: str,
        filename: str,
        starting_page: int,
        content: Dict[str, List[str]]
    ):

    md_doc = await get_pdf_markdown(session_id=session_id, filename=filename)
    sections = content['sections']
    init_sections = sections.copy()

    logger.info(f"Initial sections: {init_sections}")
    tasks = []
    
    for page in md_doc[starting_page:]:
        extract_sections_prompt = EXTRACT_SECTIONS_PROMPT.format(sections_list=sections)
        excerpt = f"#EXCERPT:\n{page['text']}\n\n#OUTPUT:"

        tasks.append(
            asyncio.create_task(
                model.aget_completion(
                    prompt=excerpt,
                    system_prompt=extract_sections_prompt,
                    response_format={'type': 'json_object'}
                )
            )
        )
    
    sections_uncleaned = await asyncio.gather(*tasks)
    sections_uncleaned = [json_repair.loads(s) for s in sections_uncleaned]

    sections_cleaned = parse_sections(sections_uncleaned, init_sections)
    sections_cleaned = {
        re.sub(r'^Appendix \d+|^\d+.?\s+', '', k.replace(":", "")).strip(): {"text": v, "raw_section": k}
        for k, v in sections_cleaned.items() if v != ""
    }
    # sections_cleaned = {
    #     re.sub(r'^\d+\s+', '', k): v for k, v in sections_cleaned.items()
    # }

    return sections_cleaned 

             


