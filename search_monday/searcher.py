from index import Index
import os


class Searcher:
    def __init__(self, index_path: str, stopwords_path: str = None):
        self.index = Index()
        self.index.load(index_path)
        self.stopwords = set()
        if stopwords_path:
            with open(stopwords_path, 'r') as f:
                self.stopwords = {word.strip().lower() for word in f if word.strip()}

    def search_and(self, terms: list[str]) -> list[tuple[str, float]]:
        docs = set(self.index.get(terms[0]).keys())
        for term in terms[1:]:
            docs &= set(self.index.get(term).keys())
        result = []
        for doc_no in docs:
            relevance = sum(0.7 if self.index.get_in_title(term).get(doc_no) else 0.3 
                          if self.index.get(term).get(doc_no) else 0 for term in terms)
            result.append((os.path.basename(doc_no), relevance))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def search_or(self, terms: list[str]) -> list[tuple[str, float]]:
        docs = set()
        for term in terms:
            docs.update(self.index.get(term).keys())
        result = []
        for doc_no in docs:
            relevance = sum(0.7 if self.index.get_in_title(term).get(doc_no) else 0.3 
                          if self.index.get(term).get(doc_no) else 0 for term in terms)
            result.append((os.path.basename(doc_no), relevance))        
        return sorted(result, key=lambda x: x[1], reverse=True)

    def search_pos(self, terms: list[str], dist: int) -> list[str]:
        assert len(terms) == 2
        result = []
        docs1 = self.index.get(terms[0])
        docs2 = self.index.get(terms[1])
        for doc_no in set(docs1.keys()) & set(docs2.keys()):
            pos1 = docs1[doc_no]
            pos2 = set(docs2[doc_no])
            for p in pos1:
                if dist > 0:
                    if any((p + d) in pos2 for d in range(-dist, dist + 1) if d != 0):
                        result.append(os.path.basename(doc_no))
                        break
                else:
                    if any(abs(p2 - p) >= abs(dist) for p2 in pos2):
                        result.append(os.path.basename(doc_no))
                        break        
        return result

    def search_boolean(self, query: str) -> list[tuple[str, float]]:
        if not query:
            return []
        tokens = query.split()
        if len(tokens) == 1:
            return [(os.path.basename(doc_no), 1.0) 
                   for doc_no in self.index.get(tokens[0]).keys()]
        if len(tokens) % 2 != 1:
            return []
        terms = tokens[::2]
        op = tokens[1].lower()
        if op == "and":
            return self.search_and(terms)
        elif op == "or":
            return self.search_or(terms)
        elif op.startswith('/'):
            try:
                dist = int(op[1:])
                return [(filename, 1.0) for filename in self.search_pos(terms, dist)]
            except ValueError:
                return []
        return []

    def search(self, query: str) -> list[int]:
        tokens= query.lower().split()
        #normalize
        
        Q = self.index.vectorize(tokens)
        relev = {}
        for doc_no in self.index.docs:
            score = self.index.get_score(Q, doc_no)
            relev[doc_no] = score
        return sorted(relev, key=relev.get, reverse=True)[:10]


if __name__ == "__main__":
    s = Searcher('index.inv', 'stopwords.txt')
    while True:
        query = input("Enter query (or 'kill' to exit): ")
        if query.lower() == 'kill':
            break
        results = s.search(query)
        if results:
            print(f"Found {len(results)} documents:")
            for filename, relevance in results:
                print(f"File {filename}: relevance {relevance}")
        else:
            print("No results found") 