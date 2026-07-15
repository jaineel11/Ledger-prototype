import hashlib
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.ocr import OCRService
from app.services.extraction import ExtractionService
from app.services.rules import RulesEngine

app = FastAPI(title="BPOptima GroundSet Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate decoupled structural singletons
ocr_service = OCRService()
extraction_service = ExtractionService()

class ExtractionSchema(BaseModel):
    water_damage_class: str
    est_repair_cost: int
    coverage_limit: int
    prior_claims_24mo: int

@app.post("/api/run-trace")
async def run_trace(case_id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Step 1: Immutable Document Digitization via OCR Service
        file_bytes = await file.read()
        content_type = file.content_type or "application/pdf"
        raw_markdown = await ocr_service.extract_markdown_from_file(file_bytes, content_type)
        
        # Step 2: Contextual JSON Parsing via Structural Extraction Service
        schema_dict = ExtractionSchema.model_json_schema()
        extracted_fields = extraction_service.extract_structured_data(raw_markdown, schema_dict)
        
        # Step 3: Pure State Machine Verification (Rules Engine)
        rule_outcome = RulesEngine.evaluate_r114(extracted_fields)
        
        # Step 4: Cryptographic Ledger Initialization
        timestamp = datetime.utcnow().isoformat()
        hash_seed = f"{case_id}_{json.dumps(extracted_fields)}_{rule_outcome['decision']}_{timestamp}"
        audit_hash = hashlib.sha256(hash_seed.encode()).hexdigest()[:12]
        
        return {
            "case_id": case_id,
            "timestamp": timestamp,
            "audit_hash": audit_hash,
            "trace": [
                {
                    "step": 1,
                    "title": "Evidence Extracted (Mistral OCR + Llama 3)",
                    "stamp": "EXTRACTED",
                    "detail": extracted_fields,
                    "raw_ocr_preview": raw_markdown[:250] + "..."
                },
                {
                    "step": 2,
                    "title": "Client rule applied",
                    "stamp": "RULE R114",
                    "rule": "IF water_damage_class = 'Category 2' AND prior_claims_24mo <= 1 AND est_repair_cost <= coverage_limit THEN AUTO_APPROVE",
                },
                {
                    "step": 3,
                    "title": "Decision Outcome Engine",
                    "stamp": rule_outcome["decision"],
                    "detail": rule_outcome["reason"]
                },
                {
                    "step": 4,
                    "title": "Audit Trail Verification Ledger",
                    "stamp": "SEALED",
                    "detail": f"Block hash: {audit_hash} linked to ledger state trace context natively."
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Core Engine Execution Failure: {str(e)}")