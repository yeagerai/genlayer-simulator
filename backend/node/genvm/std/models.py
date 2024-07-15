# backend/node/genvm/std/models.py

from sentence_transformers import SentenceTransformer


def get_model(model: str = "paraphrase-MiniLM-L6-v2"):
    return SentenceTransformer(model)
