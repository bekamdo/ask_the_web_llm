import os
from dotenv import load_dotenv
from pathlib import Path


class Config:
    _env_path = Path(__file__).parent.parent / '.env'
    print(f"Loading .env from: {_env_path}")
    load_dotenv(_env_path)

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SEARCH_API_PROVIDER = os.getenv("SEARCH_API_PROVIDER", "duckduckgo").lower()
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            available_vars = {k: v for k, v in os.environ.items() if "API" in k}
            raise ValueError(
                "OPENAI_API_KEY not found!\n"
                f"Checked path: {cls._env_path}\n"
                f"Existing API vars: {available_vars}"
            )