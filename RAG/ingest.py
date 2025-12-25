from sentence_transformers import SentenceTransformer
import numpy as np

def load_corpus(path: str):
    with open(path, "r", encoding="utf-8") as f:
        docs = [line.strip() for line in f if line.strip()]
    return docs

def embed_corpus(docs, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(docs, convert_to_numpy=True, show_progress_bar=True)
    return embeddings

if __name__ == "__main__":
    docs = load_corpus("data/corpus.txt")
    embeddings = embed_corpus(docs)
    np.save("corpus_embeddings.npy", embeddings)
