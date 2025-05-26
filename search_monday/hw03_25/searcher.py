import os
from index import Index


class Searcher:
    def __init__(self, index_path: str):
        self.index = Index()
        self.index.load(index_path)

    def search_and(self, terms: list[str]) -> list[int]:
        docs = set(self.index.get(terms[0]))
        for term in terms[1:]:
            docs &= set(self.index.get(term))
        return list(docs)

    def search_pos(self, terms: list[str], dist: int) -> list[int]:
        assert dist > 0
        assert len(terms) == 2
        result = []
        docs1 = self.index.get(terms[0])
        docs2 = self.index.get(terms[1])
        for (doc_no, pos1) in docs1.items():
            pos2 = docs2.get(doc_no)
            if pos2:
                pos2_set: set[int] = set(pos2)
                for p in pos1:
                    if (p + dist) in pos2_set:
                        result.append(doc_no)
        return result

    def search_boolean(self, query: str) -> list[int]:
        tokens = query.split()
        if len(tokens) == 1:
            return list(self.index.get(tokens[0]).keys())
        assert len(tokens) % 2 == 1
        terms = tokens[::2]
        op = tokens[1]
        if op.lower() == "and":
            return self.search_and(terms)
        elif op.startswith('/'):
            dist = int(op[1:])
            return self.search_pos(terms, dist)

    def search(self, query: str) -> list[int]:
        tokens = query.lower().split()
        # normalize
        Q = self.index.vectorize(tokens)
        relev = {}
        for doc_no in range(len(self.index.docs)):
            score = self.index.get_score(Q, doc_no)
            relev[doc_no] = score

        sorted_docs = sorted(relev.items(), key=lambda x: x[1], reverse=True)[:10]

        for i, (doc_no, score) in enumerate(sorted_docs, 1):
            file_name = os.path.basename(self.index.docs[doc_no])
            print(f"{i}. {file_name} ({score:.4f})")

        return [doc_no for doc_no, _ in sorted_docs]


if __name__ == "__main__":
    s = Searcher('index.inv')
    query = input("Enter query: ")
    s.search(query)
