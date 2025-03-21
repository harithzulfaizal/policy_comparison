IS_TOC_PROMPT = """The current page number is {page_num}.

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