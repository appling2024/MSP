import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, docs, embeddings_path):
        self.docs = docs
        self.embeddings = np.load(embeddings_path)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, query, top_k=3):
        query_emb = self.model.encode([query], convert_to_numpy=True)
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_idx = scores.argsort()[-top_k:][::-1]
        return [self.docs[i] for i in top_idx]
