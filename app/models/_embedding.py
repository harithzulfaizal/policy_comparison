import os
from typing import List

from openai import AsyncOpenAI


class AsyncOpenAIEmbedding:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            deployment_name: str
            ):
        self.base_url = base_url
        self.api_key = api_key
        self.deployment_name = deployment_name

        self.client = AsyncOpenAI(
            api_key = self.api_key,
            azure_endpoint = self.base_url,
        )
    
    async def aembed_query(self, user_query: str) -> List[float]:
        response = await self.client.embeddings.create(
            input = user_query,
            model = self.deployment_name
        )

        return response.data[0].embedding