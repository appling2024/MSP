import json
import os

class Searcher:
    def __init__(self, index_path: str, stopwords_path: str = None):
        self.index, self.docs = self.load_index(index_path)
        self.stopwords = self.load_stopwords(stopwords_path)

    def load_index(self, index_path: str) -> tuple[dict, list]:
        with open(index_path, 'r') as f:
            data = json.load(f)
            return data["index"], data["docs"]
        
    def load_doclist(self, doclist_path: str) -> list:
        with open(doclist_path, 'r') as f:
            data = json.load(f)
            return data["docs"]    
        
    def load_stopwords(self, stopwords_path: str) -> set:
        if stopwords_path:
            with open(stopwords_path, 'r') as f:
                return set(word.strip().lower() for word in f if word.strip())
        return set()   

    def search_and(self, terms: list[str]) -> list[int]:
        terms = [t for t in terms if t not in self.stopwords]
        if not terms:
            return []
        docs = set(self.index.get(terms[0], []))
        for term in terms[1:]:
            docs &= set(self.index.get(term, []))
        return sorted(docs)
    
    def search_or(self, terms: list[str]) -> list[int]:
        terms = [t for t in terms if t not in self.stopwords]
        result = set()
        for term in terms:
            result |= set(self.index.get(term, []))
        return sorted(result)

    def search(self, query: str) -> list[str]:
        query = query.lower()
        if ' or ' in query:
            terms = query.split(' or ')
            doc_ids = self.search_or(terms)
        elif ' and ' in query:
            terms = query.split(' and ')
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
        query = input("Query -> word1 and/or word2 (type 'exit' to kill): ")
        if query.strip().lower() == 'exit':
            break
        result = s.search(query)
        print("Result:", result)
