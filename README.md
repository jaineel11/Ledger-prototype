# BPOptima GroundSet - Prototype

An interactive, deterministic ledger prototype built for the BPOptima FDE take-home assignment. 

This project demonstrates a production-grade architecture for enterprise AI adoption, prioritizing determinism, auditability, and clear lineage over generative variability.

## Architecture
* **Frontend:** Vanilla HTML/JS/CSS. An interactive ledger UI that replaces the traditional "chat box" with a strict state-machine visualizer.
* **Backend:** FastAPI.
* **Digitization:** Mistral OCR (`mistral-ocr-latest`) for robust document parsing.
* **Extraction:** Groq (`llama3-70b-8192`) for strict JSON schema coercion.
* **Rules Engine:** Pure Python.

## How to Run Locally

### 1. Backend Setup
Navigate to the backend directory and set up the Python environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt