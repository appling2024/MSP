from ingest import load_corpus
from retrieve import Retriever
from generate import Generator
from evaluate import semantic_similarity

def main():
    docs = load_corpus("data/corpus.txt")
    retriever = Retriever(docs, "corpus_embeddings.npy")
    generator = Generator()

    query = input("Введите вопрос: ")

    contexts = retriever.retrieve(query)
    answer = generator.generate_answer(query, contexts)

    print("\n--- Ответ ---")
    print(answer)

    # пример оценки
    reference = contexts[0]
    score = semantic_similarity(answer, reference)
    print(f"\nSemantic similarity: {score:.3f}")

if __name__ == "__main__":
    main()
