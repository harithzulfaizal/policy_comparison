import asyncio
import json
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type, wait_exponential
from typing import List, Any, Optional, Dict, List

from openai import AsyncOpenAI, OpenAI


system_prompt = """Formatting re-enabled.
    You are a helpful assistant.
    Any indication of the output formatted within rows and/or columns should be a tabular output.
    Any code output should be contained within the markdown block ```.
    Tabular output should be in proper markdown without the markdown block ```."""


class AsyncOpenAICompletion:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            deployment_name: str = None,
            temperature: float = 0.7,
            system_prompt: str = system_prompt
            ):
        
        self.base_url = base_url
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.temperature = temperature
        self.system_prompt = system_prompt

        self.client = AsyncOpenAI(
            api_key = self.api_key,
            base_url = self.base_url,
        )
    def _create_messages(
            self,
            prompt: str,
            img_url: Optional[str] = None,
            chat_history: Optional[List] = None
            ) -> List[Dict[str, str]]:
        
        messages = [{'role': 'system', 'content': self.system_prompt}]
        
        if chat_history:
            messages.extend([{'role': m['role'], 'content': m['content']} for m in chat_history])
        
        if img_url:
            messages.append(
                {'role': 'user',
                 'content': [
                     {
                         'type': 'text',
                         'text': prompt,
                     },
                     {
                         'type': 'image_url',
                         'image_url': {'url': img_url} # f"data:image/jpeg;base64,{base64_image}
                     }
                 ]}
            )
            return messages

        messages.append({'role': 'user', 'content': prompt})
        return messages
    
    async def aget_completion(
            self,
            prompt: str,
            img_url: Optional[str] = None,
            chat_history: Optional[List] = None,
            response_format: Any = {"type": "json_object"}
            ):
        
        messages = self._create_messages(prompt=prompt, img_url=img_url,chat_history=chat_history) 

        response = await self.client.beta.chat.completions.parse(
            model=self.deployment_name,
            messages=messages, # type: ignore
            max_tokens=16384,
            response_format=response_format,
        )

        return response.choices[0].message.content 