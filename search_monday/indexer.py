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
                for pos, line in enumerate(fh):
                    tokens = line.strip().lower().split()
                    for token_pos, token in enumerate(tokens):
                        self.index.add(doc_no, token, token_pos, is_title=(pos == 0))
        self.index.finalize()
        self.index.save("index.inv")


if __name__ == "__main__":
    path = "small"
    i = Indexer(path)
