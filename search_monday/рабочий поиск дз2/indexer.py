import os
import os.path
from index import Index


class Indexer:
    def __init__(self, path: str):
        index = Index()
        for fname in os.listdir(path):
            if not fname.endswith('.txt'):
                continue
            fullpath = os.path.join(path, fname)
            doc_no = index.add_doc(fullpath)
            pos = 0
            line_no = 0
            with open(fullpath, encoding='utf8') as fh:
                for line in fh:
                    tokens = line.strip().lower().split()
                    for token in tokens:
                        index.add(doc_no, token, pos, line_no == 0)
                        pos += 1
                    line_no += 1
        index.save('index.inv')


if __name__ == "__main__":
    path = "small"
    i = Indexer(path)
