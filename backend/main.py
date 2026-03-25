from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
os.makedirs("uploads", exist_ok=True)
from risk_score import calculate_risk_score
from ocr import extract_text
from parser import extract_lab_values
from abnormality import detect_abnormal
from summary import generate_summary
from copilot import build_vector_store, query_copilot
from prescription import analyze_prescription   # NEW IMPORT
from alert_system import check_critical_alerts, generate_medical_alerts

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

# Global variables for AI Copilot
vector_index = None
documents = None


# -----------------------------
# Emergency alert system
# -----------------------------


# -----------------------------
# Disease prediction
# -----------------------------
def predict_disease(values):

    diseases = []

    if values.get("Hemoglobin", 20) < 12:
        diseases.append("Possible Anemia")

    if values.get("White_Blood_Cells", 0) > 11000:
        diseases.append("Possible Infection")

    if values.get("Glucose", 0) > 125:
        diseases.append("Possible Diabetes")

    return diseases


# -----------------------------
# Upload and analyze lab report
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

    # Generate summary
    summary = generate_summary(abnormal)

    # Emergency alerts
    alerts = check_critical_alerts(abnormal)
    medical_alerts = generate_medical_alerts(values)
    # Disease prediction
    diseases = predict_disease(values)

    return {

        # "extracted_text": text,
        # "values": values,
        "abnormalities": abnormal,
        "risk_score": risk,
        "summary": summary,
        "alerts": alerts,
        "possible_conditions": diseases

    }


# -----------------------------
# Prescription analysis endpoint
# -----------------------------
@app.post("/analyze_prescription")

async def analyze_prescription_api(file: UploadFile):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_prescription(path)

    return result


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)