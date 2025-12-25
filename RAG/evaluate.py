from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_similarity(answer, reference):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb = model.encode([answer, reference], convert_to_numpy=True)
    return cosine_similarity([emb[0]], [emb[1]])[0][0]
