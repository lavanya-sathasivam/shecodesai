# AI Medical Intelligence Dashboard

An AI-powered healthcare analysis platform that processes lab reports and prescriptions using OCR, machine learning, and medical knowledge bases.

## Features

### 🏥 Lab Report Analysis
- **OCR Processing**: Extracts text from lab report images using EasyOCR with Tesseract fallback
- **Value Extraction**: Parses lab values using regex pattern matching
- **Abnormality Detection**: Compares values against reference ranges
- **Health Risk Scoring**: Calculates 0-100 risk score with status indicators
- **Medical Alerts**: Generates critical alerts for severe conditions
- **Disease Prediction**: Rule-based assessment for anemia, infections, diabetes
- **Data Visualization**: Bar charts for abnormal test values

### 💊 Prescription Analyzer
- **Prescription OCR**: Reads text from prescription images
- **Medicine Detection**: Hybrid approach using fuzzy string matching + semantic similarity
- **Drug Interaction Checking**: Identifies dangerous medication combinations with warnings

### 🤖 AI Medical Copilot
- **Vector-Based Knowledge**: Uses FAISS and Sentence Transformers for semantic search
- **Contextual Answers**: Provides medical insights based on user's lab report + knowledge base
- **Interactive Q&A**: Ask questions about lab results and get AI-powered responses

## Technology Stack

### Backend (Python/FastAPI)
- **FastAPI**: REST API framework
- **EasyOCR + Tesseract**: Optical character recognition
- **Sentence Transformers**: Text embeddings for semantic similarity
- **FAISS**: Vector similarity search
- **Pandas**: Data processing
- **RapidFuzz**: Fuzzy string matching

### Frontend (Next.js/React)
- **Next.js 16**: React framework
- **Chart.js**: Data visualization
- **Tailwind CSS**: Styling
- **Responsive Design**: Mobile-friendly interface

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend
```bash
cd backend
# Activate virtual environment if not already
python main.py
```
Backend will run on http://127.0.0.1:8000

### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on http://localhost:3000

## Usage

1. **Lab Report Analysis**:
   - Upload a lab report image (JPG/PNG)
   - Click "Analyze Report"
   - View risk score, abnormalities, alerts, and chart

2. **Prescription Analysis**:
   - Upload prescription image
   - Click "Analyze Prescription"
   - See detected medicines and interaction warnings

3. **AI Copilot**:
   - First, build context by uploading lab report (this indexes the report for Q&A)
   - Ask questions about your results
   - Get AI-powered medical insights

## Data Files

- `dataset/reference_ranges.csv`: Normal ranges for blood tests
- `dataset/medicine_dataset.csv`: Comprehensive medicine database
- `dataset/medical_knowledge_base.csv`: Combined knowledge base (generated via combine.py)
- `dataset/drugs_side_effects.csv`: Side effects database

## API Endpoints

- `POST /analyze`: Analyze lab report
- `POST /analyze_prescription`: Analyze prescription
- `POST /build_report_context`: Index report for AI copilot
- `POST /ask`: Query AI copilot

## Project Structure

```
shecodesai/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── ocr.py                  # Text extraction
│   ├── parser.py               # Lab value parsing
│   ├── abnormality.py          # Abnormality detection
│   ├── risk_score.py           # Risk calculation
│   ├── summary.py              # Medical summaries
│   ├── alert_system.py         # Medical alerts
│   ├── prescription.py         # Prescription analysis
│   ├── copilot.py              # AI knowledge base
│   ├── medicine_info.py        # Medicine utilities
│   ├── dataset/                # CSV data files
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.js             # Main dashboard
│   │   ├── layout.js           # App layout
│   │   └── globals.css         # Global styles
│   ├── package.json            # Node dependencies
│   └── public/                 # Static assets
└── README.md                   # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and research purposes. Please consult healthcare professionals for medical advice.

## Disclaimer

This application is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about medical conditions.