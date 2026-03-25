from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []

# load dataset
knowledge_df = pd.read_csv("dataset/medical_knowledge_base.csv")

# use correct column
knowledge_docs = knowledge_df["name"].tolist()


def build_vector_store(text):

    global documents

    report_docs = text.split("\n")

    documents = report_docs + knowledge_docs

    embeddings = model.encode(documents)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, documents


def query_copilot(question, index, documents):

    q_embedding = model.encode([question])

    D, I = index.search(np.array(q_embedding), k=3)

    context = "\n".join([documents[i] for i in I[0]])

    answer = f"Based on your report:\n{context}"

    return answer