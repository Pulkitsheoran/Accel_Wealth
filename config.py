import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL_NAME = os.getenv("FINBERT_MODEL_PATH", "ProsusAI/finbert")
    BASE_URL = "https://openrouter.ai/api/v1"
    HF_TOKEN = os.getenv("HF_TOKEN")
    # Updated list including the heavy 120B model
    FREE_MODELS = [
        "nvidia/nemotron-3-super-120b-a12b:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "google/gemma-3-27b-it:free",
    ]

    LLM_MODEL = FREE_MODELS[0]

    @classmethod
    def validate(cls):
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("CRITICAL: OPENROUTER_API_KEY is missing from .env!")
