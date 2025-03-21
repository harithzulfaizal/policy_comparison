from typing import List, Optional, Dict, Any

from app.models._llm import AsyncOpenAICompletion

class BaseLLMChain:
    """Base chain for LLM interactions."""
    
    def __init__(self, llm: AsyncOpenAICompletion, prompt: str):
        self.llm = llm
        self.prompt = prompt

    async def acall(
        self,
        input_variables: Optional[Dict[str, Any]] = None,
        img_url: Optional[str] = None,
        chat_history: Optional[List] = None,
        response_format: Optional[Dict[str, str]] = {"type": "json_object"}
    ) -> str:

        formatted_prompt = self.prompt.format_map(input_variables) if input_variables else self.prompt
        return await self.llm.aget_completion(
            prompt=formatted_prompt,
            img_url=img_url,
            chat_history=chat_history,
            response_format=response_format
        )  # type: ignore