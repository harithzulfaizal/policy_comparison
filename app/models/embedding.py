import os

from app.models._embedding import AsyncOpenAIEmbedding

embedding = AsyncOpenAIEmbedding(
    base_url=os.getenv("GEMINI_BASE_URL"),
    api_key=os.getenv("GEMINI_API_KEY"),
    deployment_name=os.getenv("GEMINI_EMBEDDING_MODEL")
)