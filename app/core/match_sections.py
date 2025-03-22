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


async def compare_document_sections(
        sections_A: List[str],
        sections_B: List[str],
    ):

    prompt = (
        f"#SECTIONS LIST FROM VERSION A: {list(sections_A.keys)}\n"
        f"#SECTIONS LIST FROM VERSION B: {list(sections_B.keys)}\n"
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
            match = process.
