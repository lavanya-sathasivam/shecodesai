import easyocr
import pandas as pd
import re
from rapidfuzz import fuzz

# -----------------------------
# INITIALIZE OCR
# -----------------------------
reader = easyocr.Reader(['en'])

# -----------------------------
# LOAD MEDICINE DATASET
# -----------------------------
medicine_db = pd.read_csv("dataset/medicine_dataset.csv", low_memory=False)

# Extract only base medicine name
medicine_db["base_name"] = medicine_db["name"].astype(str).str.split().str[0].str.lower()

medicine_list = medicine_db["base_name"].dropna().unique().tolist()

from sentence_transformers import SentenceTransformer, util
import torch

# Lazy loading - model will be loaded when first used
model = None
medicine_embeddings = None

def get_model():
    global model, medicine_embeddings
    if model is None:
        print("Loading medicine detection model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        medicine_embeddings = model.encode(medicine_list, convert_to_tensor=True)
        print("Medicine detection model loaded!")
    return model, medicine_embeddings
# -----------------------------
# OCR PRESCRIPTION READER
# -----------------------------
def read_prescription(image_path):

    results = reader.readtext(image_path)

    text = ""

    for r in results:
        text += r[1] + " "

    return text


# -----------------------------
# TEXT CLEANING
# -----------------------------
def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def detect_medicines(text):

    detected = []

    text = clean_text(text)

    words = text.split()

    words = [w for w in words if len(w) > 3]

    for word in words:

        # fuzzy matching first
        for med in medicine_list:

            score = fuzz.ratio(word, med)

            if score > 90:
                detected.append(med)

    # Only load model if we have potential medicines to check
    if words:
        model, medicine_embeddings = get_model()

        for word in words:
            word_embedding = model.encode(word, convert_to_tensor=True)

            similarities = util.cos_sim(word_embedding, medicine_embeddings)[0]

            best_idx = torch.argmax(similarities)

            if similarities[best_idx] > 0.80:
                detected.append(medicine_list[best_idx])

    return list(set(detected))
# -----------------------------
# DRUG INTERACTION CHECK
# -----------------------------
def check_interactions(meds):

    interactions = {

        ("ibuprofen", "aspirin"):
        "Taking Ibuprofen with Aspirin may increase bleeding risk.",

        ("paracetamol", "alcohol"):
        "Combining Paracetamol with alcohol may cause liver damage.",

        ("amoxicillin", "methotrexate"):
        "Amoxicillin may increase Methotrexate toxicity."

    }

    warnings = []

    for i in range(len(meds)):
        for j in range(i + 1, len(meds)):

            pair = (meds[i], meds[j])
            reverse = (meds[j], meds[i])

            if pair in interactions:
                warnings.append(interactions[pair])

            elif reverse in interactions:
                warnings.append(interactions[reverse])

    if not warnings:
        warnings.append("No dangerous drug interactions detected.")

    return warnings


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def analyze_prescription(image_path):

    text = read_prescription(image_path)

    medicines = detect_medicines(text)

    warnings = check_interactions(medicines)

    return {

        "extracted_text": text,
        "medicines": medicines,
        "interaction_warnings": warnings

    }