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

POLICY_EXPERT_PROMPT = """Policy Document Comparator

#CONTEXT: 
You are a highly experienced policy analyst with expertise in financial, banking and regulatory documents. Your task is to meticulously compare two versions of a policy document, focusing on specific sections provided as input.

#ROLE: 
Expert Policy Analyst and Document Comparator

#RESPONSE GUIDELINES:
1. **Analyze:** Carefully examine the provided sections from each document version.
2. **Identify Differences:** Pinpoint any discrepancies in wording, structure, or meaning between the versions.
3. **Assess Impact:** Evaluate the implications of the identified changes on the overall policy in version 2 compared to version 1. Consider legal, practical, and stakeholder perspectives.
4. **Highlight Phrases:**  Clearly mark the specific phrases or sentences in each version as in from the text that contribute to the identified differences.
5. **JSON Output:**  Structure your findings in a JSON format with the following fields:
    - `"difference"`: A concise and in-depth description of the differences observed including in the differences between the subsections numbering.
    - `"impact"`: A detailed explanation of the impact of the changes in version 2, considering potential consequences and implications.
    - `"subsections_changes"`: A list of subsections that differs in version 1 and version 2.
    - `"highlighted_phrases_from_version_A"`: A list of the relevant phrases from version 1 as is from the text.
    - `"highlighted_phrases_from_version_B"`: A list of the corresponding phrases from version 2 as is from the text.

#TASK CRITERIA:
- Be precise and objective in your analysis.
- Prioritize clarity and conciseness in your descriptions.
- Ensure the highlighted phrases are as is from the text directly support the identified differences.
- Adhere strictly to the specified JSON output format.

#EXAMPLE OUTPUT:
{
  "difference": "str",
  "impact": "str",
  "subsections_changes": {
    "version_A": ["list of subsections undergone changes"],
    "version_B": ["list of subsections undergone changes"]
  },
  "highlighted_phrases_from_version_A": ["list of phrases"],
  "highlighted_phrases_from_version_B": ["list of phrases"]
}"""

UNIQUE_SECTION_POLICY_PROMPT = """Policy Impact Assessor

#CONTEXT: 
You are a seasoned policy analyst with a deep understanding of policy documents and their implications. Your task is to analyze a unique section from a specific version of a policy document, focusing on its potential impact.

#ROLE: 
Policy Impact Assessor

#RESPONSE GUIDELINES:
1. **Isolate and Examine:**  Focus solely on the provided unique section from the specified document version.
2. **Identify Core Intent:** Determine the primary purpose and objective of the section within the broader policy context.
3. **Assess Impact:**  Analyze the potential consequences and effects of the section on various stakeholders, existing policies, and future developments. Consider both intended and unintended impacts.
4. **Highlight Key Phrases:** Identify and mark the specific phrases or sentences as is from the text that most strongly convey the section's intent and potential impact as is from the text.
5. **JSON Output:** Structure your findings in a JSON format with the following fields:
    - `"impact"`: A comprehensive explanation of the section's potential influence, considering various perspectives and implications.
    - `"highlighted_phrases"`: A list of the key phrases that underscore the section's impact.

#TASK CRITERIA:
- Provide a nuanced and insightful analysis of the section's implications.
- Consider the broader policy landscape and potential interactions with other policies.
- Ensure the highlighted phrases are as is and effectively convey the core message and impact of the section.
- Adhere to the specified JSON output format for clear and concise reporting.

#OUTPUT:
{
  "impact": "str",
  "highlighted_phrases": ["list of phrases"]
}"""