import os
import re
import asyncio
import aiofiles
from typing import List, Dict
from pydantic import BaseModel

import base64
import pymupdf4llm
import json_repair
from rapidfuzz import fuzz, process, utils

from app.config import ROOT_DIR
from app.logger import logger
from app.core.prompts import SECTION_MATCHING_PROMPT
from app.models.llm import model

class MatchSections(BaseModel):
    matching_sections: List[str]
    sections_unique_to_version_A: List[str]
    sections_unique_to_version_B: List[str]


async def match_document_sections(
        sections_A: Dict[str, str],
        sections_B: Dict[str, str],
    ):

    sections_A_list = list(re.sub(r'^\d+\s+', '', k) for k in sections_A.keys())
    sections_B_list = list(re.sub(r'^\d+\s+', '', k) for k in sections_B.keys())

    prompt = (
        f"#SECTIONS LIST FROM VERSION A: {sections_A_list}\n"
        f"#SECTIONS LIST FROM VERSION B: {sections_B_list}\n"
        "\n#OUTPUT:"
    )

    response = await model.aget_completion(
        prompt=prompt,
        system_prompt=SECTION_MATCHING_PROMPT,
        response_format=MatchSections
    )

    response = json_repair.loads(response)
    print(response)

    matching_sections = response['matching_sections']
    sections_unique_to_version_A = response['sections_unique_to_version_A']
    sections_unique_to_version_B = response['sections_unique_to_version_B']

    for sections in [sections_unique_to_version_A, sections_unique_to_version_B]:
        for section in sections.copy():
            match = process.extractOne(
                query=section,
                choices=matching_sections,
                # score_cutoff=90,
                scorer=fuzz.WRatio,
                processor=utils.default_process)

            if match[1] >= 90: sections.remove(section)

    sections_info = {
        'matching_sections': matching_sections,
        'sections_unique_to_version_A': sections_unique_to_version_A,
        'sections_unique_to_version_B': sections_unique_to_version_B,
    }

    return {
        'sections_info': sections_info,
        'sections_A': sections_A,
        'sections_B': sections_B,
    }