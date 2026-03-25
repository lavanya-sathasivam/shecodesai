from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

# Lazy loading
model = None
knowledge_docs = None

def get_model_and_knowledge():
    global model, knowledge_docs
    if model is None:
        print("Loading AI copilot model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        # load dataset
        knowledge_df = pd.read_csv("dataset/medical_knowledge_base.csv")
        # use correct column
        knowledge_docs = knowledge_df["name"].tolist()
        print("AI copilot model loaded!")
    return model, knowledge_docs


def build_vector_store(text):

    model, knowledge_docs = get_model_and_knowledge()

    report_docs = text.split("\n")

    documents = report_docs + knowledge_docs

    embeddings = model.encode(documents)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, documents


def query_copilot(question, index, documents):

    model, _ = get_model_and_knowledge()

    q_embedding = model.encode([question])

    D, I = index.search(np.array(q_embedding), k=3)

    context = "\n".join([documents[i] for i in I[0]])

    answer = f"Based on your report:\n{context}"

    return answer