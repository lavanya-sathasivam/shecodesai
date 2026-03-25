from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import shutil

from risk_score import calculate_risk_score
from ocr import extract_text
from parser import extract_lab_values
from abnormality import detect_abnormal
from summary import generate_summary
from copilot import build_vector_store, query_copilot

app = FastAPI()

# Global variables for AI Copilot
vector_index = None
documents = None


# -----------------------------
# Upload and analyze report
# -----------------------------
@app.post("/analyze")

async def analyze(file: UploadFile):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text = extract_text(path)

    # Extract lab values
    values = extract_lab_values(text)

    # Detect abnormalities
    abnormal = detect_abnormal(values)

    # Calculate risk score
    risk = calculate_risk_score(abnormal)

    # Generate patient summary
    summary = generate_summary(abnormal)

    return {

        "extracted_text": text,
        "values": values,
        "abnormalities": abnormal,
        "risk_score": risk,
        "summary": summary

    }


# -----------------------------
# Build report context for AI Copilot
# -----------------------------
class ReportText(BaseModel):
    text: str


@app.post("/build_report_context")

def build_context(data: ReportText):

    global vector_index, documents

    vector_index, documents = build_vector_store(data.text)

    return {"message": "Report indexed for AI copilot"}


# -----------------------------
# Ask AI Copilot questions
# -----------------------------
class Question(BaseModel):
    question: str


@app.post("/ask")

def ask_question(data: Question):

    global vector_index, documents

    if vector_index is None:
        return {"error": "Report context not built yet"}

    answer = query_copilot(data.question, vector_index, documents)

    return {"answer": answer}