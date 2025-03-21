import os

from app.models._llm import AsyncOpenAICompletion

gemini_2_flash = AsyncOpenAICompletion(
    base_url=os.getenv("GEMINI_BASE_URL"),
    api_key=os.getenv("GEMINI_API_KEY"),
    deployment_name=os.getenv("GEMINI_2_FLASH_MODEL"),
)
