from pydantic import BaseSettings
from functools import lru_cache
import os


class Config(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "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")
    
    
@lru_cache()
def get_config():
    return Config()
    