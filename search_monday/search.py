import json
import os

class Searcher:
    def __init__(self, index_path: str, stopwords_path: str = None):
        self.index, self.docs = self.load_index(index_path)
        self.stopwords = self.load_stopwords(stopwords_path)

    def load_index(self, index_path: str) -> tuple[dict, list]:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["index"], data["docs"]

    def load_doclist(self, doclist_path: str) -> list:
        with open(doclist_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["docs"]

    def load_stopwords(self, stopwords_path: str) -> set:
        if stopwords_path:
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f if word.strip())
        return set()

    def search_and(self, terms: list[str]) -> list[int]:
        terms = [t for t in terms if t not in self.stopwords]
        if not terms:
            return []
        first_term_docs = set(map(int, self.index.get(terms[0], {}).keys()))
        for term in terms[1:]:
            term_docs = set(map(int, self.index.get(term, {}).keys()))
            first_term_docs &= term_docs
        return sorted(first_term_docs)

    def search_or(self, terms: list[str]) -> list[int]:
        terms = [t for t in terms if t not in self.stopwords]
        result = set()
        for term in terms:
            term_docs = set(map(int, self.index.get(term, {}).keys()))
            result |= term_docs
        return sorted(result)

    def search_pos(self, terms: list[str], dist: int) -> list[int]:
        assert dist > 0
        assert len(terms) == 2
        result = set()
        docs1 = self.index.get(terms[0])
        docs2 = self.index.get(terms[1])
        for doc_no, pos1 in docs1.items():
            if doc_no in docs2:
                pos2 = docs2.get(doc_no)
                if pos2:
                    pos2_set: set[int] = set(pos2)
                    for p in pos1:
                        if (p + dist) in pos2_set:
                            result.add(int(doc_no))
                            break  # достаточно одного совпадения в документе
        return sorted(result)



    def search(self, query: str) -> list[str]:
        query = query.lower().strip()
        if ' or ' in query:
            terms = query.split(' or ')
            doc_ids = self.search_or(terms)
        elif ' and ' in query:
            terms = query.split(' and ')
            doc_ids = self.search_and(terms)
        elif '/' in query:
            parts = query.split()
            terms = [p for p in parts if not p.startswith('/')]
            ops = [p for p in parts if p.startswith('/')]
            if ops:
                dist = int(ops[0][1:])
                doc_ids = self.search_pos(terms, dist)
            else:
                doc_ids = self.search_and(terms)
        else:
            terms = query.split()
            doc_ids = self.search_and(terms)
        return [os.path.basename(self.docs[doc_id]) for doc_id in doc_ids]

if __name__ == '__main__':
    s = Searcher(
        'C:/Users/user/Documents/GitHub/MSP/search_monday/index.inv',
        'C:/Users/user/Documents/GitHub/MSP/search_monday/stopwords.txt'
    )
    while True:
        query = input("Query -> word1 and/or word2 or 'word1 word2 /3' (type 'exit' to kill): ")
        if query.strip().lower() == 'exit':
            break
        result = s.search(query)
        print("Result:", result)
