# backend/node/genvm/std/models.py

from sentence_transformers import SentenceTransformer

DEFAULT_MODEL_NAME = "paraphrase-MiniLM-L6-v2"


def get_model(model_name: str = None):
    model = model_name if model_name is not None else DEFAULT_MODEL_NAME
    return SentenceTransformer(model)
