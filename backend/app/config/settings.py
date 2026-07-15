import os
from pathlib import Path
from dotenv import load_dotenv

# Locate base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    
    MISTRAL_OCR_MODEL: str = os.getenv("MISTRAL_OCR_MODEL", "mistral-ocr-latest")
    GROQ_EXTRACTION_MODEL: str = os.getenv("GROQ_EXTRACTION_MODEL", "llama3-70b-8192")
    
    PROMPT_DIR: Path = BASE_DIR / "app" / "prompts"

settings = Settings()