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
from itertools import zip_longest

from app.config import ROOT_DIR
from app.logger import logger
from app.core.prompts import POLICY_EXPERT_PROMPT, UNIQUE_SECTION_POLICY_PROMPT
from app.models.llm import model

async def process_matching_sections(matching_sections, sections_A, sections_B):
    tasks_ms = []

    for section in matching_sections:
        text1 = sections_A.get(section, {}).get('text')
        if not text1:
            closest_section = process.extractOne(section, list(sections_A.keys()))[0]
            text1 = sections_A.get(closest_section, {}).get('text')

        text2 = sections_B.get(section, {}).get('text')
        if not text2:
            closest_section = process.extractOne(section, list(sections_B.keys()))[0]
            text2 = sections_B.get(closest_section, {}).get('text')

        user_prompt = f"""#SECTION EXCERPT FROM VERSION 1: {text1}
        #SECTION EXCERPT FROM VERSION 2: {text2}

        #OUTPUT:"""

        task = asyncio.create_task(
            model.aget_completion(
                system_prompt=POLICY_EXPERT_PROMPT,
                prompt=user_prompt,
                response_format={"type": "json_object"}
            )
        )
        tasks_ms.append(task)

    responses = await asyncio.gather(*tasks_ms)
    return [json_repair.loads(r) for r in responses]


async def compare_sections(
        sections_info: Dict[str, List[str]],
        sections_A: Dict[str, str],
        sections_B: Dict[str, str],
        ):

    print(sections_info)

    sections_ordered = []

    for section_A, section_B in zip_longest(list(sections_A.keys()), list(sections_B.keys())):
        if section_A == section_B:
            sections_ordered.append(section_A)
        elif section_A != section_B:
            if section_B not in sections_ordered and section_B is not None:    
                sections_ordered.append(section_B)
            if section_A not in sections_ordered and section_A is not None:
                sections_ordered.append(section_A)
        elif section_A is None:
            sections_ordered.append(section_B)
        elif section_B is None:
            sections_ordered.append(section_A)

    matching_sections = sections_info["matching_sections"]
    ms_dict = {}
    # tasks_ms = []

    # for section in matching_sections:
    #     # print("============================================================================================================")
    #     try:
    #         text1 = sections_A[section]['text']
    #     except:
    #         closest_section = process.extractOne(section, list(sections_A.keys()))[0]
    #         text1 = sections_A[closest_section]['text']
        
    #     try:
    #         text2 = sections_B[section]['text']
    #     except:
    #         closest_section = process.extractOne(section, list(sections_B.keys()))[0]
    #         text2 = sections_B[closest_section]['text']

    #     user_prompt = f"""#SECTION EXCERPT FROM VERSION 1: {text1}
    #     #SECTION EXCERPT FROM VERSION 2: {text2}

    #     #OUTPUT:"""

    #     task = asyncio.create_task(
    #         model.aget_completion(
    #             system_prompt=POLICY_EXPERT_PROMPT,
    #             prompt=user_prompt,
    #             response_format={"type": "json_object"}
    #             )
    #         )
    #     tasks_ms.append(task)

    # responses = await asyncio.gather(*tasks_ms)
    # responses = [json_repair.loads(r) for r in responses]

    responses = await process_matching_sections(matching_sections, sections_A, sections_B)

    for response, section in zip(responses, matching_sections):
        ms_dict[section] = response

    #wip
    unique_sections_v1 = [process.extractOne(usec, list(sections_A.keys()))[0] for usec in sections_info["sections_unique_to_version_A"]]
    unique_sections_v2 = [process.extractOne(usec, list(sections_B.keys()))[0] for usec in sections_info["sections_unique_to_version_B"]]

    us_dict = {}

    all_unique_sections = unique_sections_v1 + unique_sections_v2 
    tasks_us = []

    for ausec in all_unique_sections.copy():
        print(ausec)
        match = process.extractOne(ausec, ms_dict.keys())
        print(match)
        if match[1] >= 90:
            all_unique_sections.remove(ausec)

    print("NEW AUSEC ------!!!!!!!!!!!! ", all_unique_sections)

    for unique_section in all_unique_sections:
        user_prompt = f"""#SECTION EXCERPT FROM VERSION {1 if unique_section in unique_sections_v1 else 2}: {sections_A[unique_section]['text'] if unique_section in unique_sections_v1 else sections_B[unique_section]['text']}
        
        #OUTPUT:"""

        task = asyncio.create_task(
            model.aget_completion(
                system_prompt=UNIQUE_SECTION_POLICY_PROMPT,
                prompt=user_prompt,
                response_format={"type": "json_object"}
                )
            )
        tasks_us.append(task)

    responses = await asyncio.gather(*tasks_us)
    responses = [json_repair.loads(r) for r in responses]

    for unique_section, response in zip(all_unique_sections, responses):
        us_dict[unique_section] = {
            "version": 1 if unique_section in unique_sections_v1 else 2,
            "result": response
        }
        
    all_sections = []

    for section in sections_ordered:
        if section in ms_dict:
            all_sections.append(
                {   
                    "old_section_no": sections_A[process.extractOne(section, list(sections_A.keys()))[0]]['raw_section'],
                    "new_section_no": sections_B[process.extractOne(section, list(sections_B.keys()))[0]]['raw_section'],
                    "section": section,
                    "difference": ms_dict[section]['difference'],
                    "impact": ms_dict[section]['impact'],
                    "highlighted_phrases_from_version_A": ms_dict[section]['highlighted_phrases_from_version_A'],
                    "highlighted_phrases_from_version_B": ms_dict[section]['highlighted_phrases_from_version_B'],
                }
            )

        elif section in us_dict:
            all_sections.append(
                {
                    "old_section_no": sections_A[process.extractOne(section, list(sections_A.keys()))[0]]['raw_section'] if us_dict[section]['version'] == 1 else None,
                    "new_section_no": sections_B[process.extractOne(section, list(sections_B.keys()))[0]]['raw_section'] if us_dict[section]['version'] == 2 else None,
                    "section": section,
                    "difference": "",
                    "impact": us_dict[section]['result']['impact'],
                    "highlighted_phrases_from_version_A": us_dict[section]['result']['highlighted_phrases'] if us_dict[section]['version'] == 1 else [],
                    "highlighted_phrases_from_version_B": us_dict[section]['result']['highlighted_phrases'] if us_dict[section]['version'] == 2 else [],
                }
            )

    # WIP
    # for s in all_sections:
    #     os = s['old_section_no'] 
    #     ns = s['new_section_no']

    #     if os:
    #         s['old_section_no'] = re.findall(r"(?:Appendix\s+\d+|\d+)", s['old_section_no'])[0].replace(":", "").strip()
    #     if ns:
    #         s['new_section_no'] = re.findall(r"(?:Appendix\s+\d+|\d+)", s['new_section_no'])[0].replace(":", "").strip()

    return all_sections
