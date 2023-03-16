from pydantic import BaseSettings
from functools import lru_cache
import os


class Config(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    
@lru_cache()
def get_config():
    return Config()