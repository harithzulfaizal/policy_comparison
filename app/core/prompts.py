EXTRACT_TOC_PROMPT = """The current page number is {page_num}.

Given the image of a page of a document, determine whether the page contains a table of content.
If a table of contents exist, is_toc is 1. Otherwise, is_toc is 0.

Given the table of content, extract the sections including appendix titles as content.
The table of contents should be in a dict of sections as key and the list of sections as value.
If there is no table of content, output None for content.

If there is table of content:
{{
    "sections":[
        "1 Introduction",
        "2 Section XXX",
        "Section 2",
        "Section 3",
        "Appendix 2: Here is the title",
        "Appendix 4 What can be done"
    ]
}}

If there is no table of content:
{{
    "sections": []
}}"""

EXTRACT_SECTIONS_PROMPT = """You are an expert in analysing policy document. 
Based on the given excerpt of a page, only extract the section titles and section contents in JSON.
The section titles extracted must exist in {sections_list}. Extract the section titles based on the list.
Extract all the sections titles and section contents that are only available in the excerpt. If there are section contents available without section titles, use the "PREV_PAGE" as the section title.
You must adhere to the JSON formatting in the #EXAMPLE under all circumstances.

#EXAMPLE:
{{
    "1 Introduction" (str): "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "PART A Abstract" (str): "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "Introduction" (str): "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "8 Conclusion" (str): "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
}}
"""

SECTION_MATCHING_PROMPT = """You are a meticulous document analyst tasked with comparing two versions of a document. Each document is structured into sections with unique headings.
Your objective is to identify sections present in both versions and highlight the sections that are unique to each version.

#ROLE:
You are a meticulous and accurate document comparison engine.

#RESPONSE GUIDELINES:
1. Analyze the list of sections from each document version.
2. Identify sections that appear in both versions and output them in a list labeled "matching_sections".
3. Identify sections unique to each version and output them in separate lists labeled "sections_unique_to_version_A" and "sections_unique_to_version_B".

#TASK CRITERIA:
- Ensure accurate semantic relevant matching of section headings.
- Clearly distinguish between matching and unique sections.
- Present the output in a well-formatted JSON based on the example output.
- Do not under any circumstances change the sections titles from the lists given.

#EXAMPLE OUTPUT:
{
    "matching_sections": [
        "Section 1",
        "Section 2",
        "Section 3"
    ],
    "sections_unique_to_version_A": [
        "Section A",
        "Section B"
    ],
    "sections_unique_to_version_B": [
        "Section C",
        "Section D"
    ]
}
"""