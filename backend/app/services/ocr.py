import base64
from mistralai.client import Mistral
from app.config.settings import settings

class OCRService:
    def __init__(self):
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = settings.MISTRAL_OCR_MODEL

    async def extract_markdown_from_file(self, file_bytes: bytes, content_type: str) -> str:
        base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
        document_url = f"data:{content_type};base64,{base64_encoded}"

        ocr_response = self.client.ocr.process(
            model=self.model,
            document={
                "type": "document_url",
                "document_url": document_url
            }
        )
        return "\n\n".join([page.markdown for page in ocr_response.pages])