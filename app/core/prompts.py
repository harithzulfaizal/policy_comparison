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