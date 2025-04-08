import json
from pymorphy2 import MorphAnalyzer

class Index:
    def __init__(self):
        self.index = {}
        self.docs = []
        self.morph = MorphAnalyzer()

    def add_doc(self, doc_name: str) -> int:
        self.docs.append(doc_name)
        doc_no = len(self.docs) - 1
        return doc_no

    def add(self, doc_no: int, term: str) -> None:
        if term not in self.index:
            self.index[term] = [doc_no]
        elif self.index[term][-1] != doc_no:
            self.index[term].append(doc_no)

    def get(self, term: str) -> list[int]:
        return self.index.get(term, [])

    def save(self, fname: str):
        with open(fname, "w") as fh:
            json.dump({
                'index': self.index,
                'docs': self.docs
            }, fh)

    def load(self, fname: str):
        with open(fname, "r") as fh:
            temp = json.load(fh)
            self.index, self.docs = temp['index'], temp['docs']

    def get_normalized_terms(self, term: str) -> list:
        parsed = self.morph.parse(term) 
        return [p.normal_form for p in parsed]  
