import json
from groq import Groq
from app.config.settings import settings

class ExtractionService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_EXTRACTION_MODEL

    def _load_system_prompt(self, target_schema_json: str) -> str:
        prompt_path = settings.PROMPT_DIR / "extraction_prompt.txt"
        with open(prompt_path, "r") as f:
            template = f.read()
        return template.format(schema=target_schema_json)

    def extract_structured_data(self, raw_text: str, schema_dict: dict) -> dict:
        system_prompt = self._load_system_prompt(json.dumps(schema_dict))
        
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            model=self.model,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)