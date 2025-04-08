import os
import os.path
from index import Index

class Indexer:
    def __init__(self, path: str):
        self.index = Index()
        
        for fname in os.listdir(path):
            if not fname.endswith('.txt'):
                continue
            fullpath = os.path.join(path, fname)
            doc_no = self.index.add_doc(fullpath)
            with open(fullpath, encoding="utf-8") as fh:
                for line in fh:
                    tokens = line.strip().lower().split()
                    for token in tokens:
                        for lemma in self.index.get_normalized_terms(token):
                            self.index.add(doc_no, lemma)
        self.index.save(r"C:\Users\user\Documents\GitHub\MSP\search_monday\index.inv")

if __name__ == "__main__":
    path = r"C:\Users\user\Documents\GitHub\MSP\search_monday\small"
    i = Indexer(path)