import math
import json
import numpy as np
from pymorphy2 import MorphAnalyzer

class Index:
    def __init__(self):
        self.index = {}
        self.title_index = {}
        self.docs = []
        self.term2coord = {}
        self.doc_term_freqs = []
        self.doc_count = 0
        self.morph = MorphAnalyzer()

    def add_doc(self, path: str) -> int:
        self.docs.append(path)
        self.doc_term_freqs.append({})
        self.doc_count += 1
        return self.doc_count - 1

    def add(self, doc_no: int, raw_term: str, pos: int, is_title: bool):
        parse = self.morph.parse(raw_term)
        if not parse:
            return
        term = parse[0].normal_form

        if term not in self.term2coord:
            self.term2coord[term] = {}
        if doc_no not in self.term2coord[term]:
            self.term2coord[term][doc_no] = []
        self.term2coord[term][doc_no].append(pos)

        tf_map = self.doc_term_freqs[doc_no]
        tf_map[term] = tf_map.get(term, 0) + 1

        index_target = self.title_index if is_title else self.index
        if term not in index_target:
            index_target[term] = {}
        if doc_no not in index_target[term]:
            index_target[term][doc_no] = []
        index_target[term][doc_no].append(pos)

    def get(self, raw_term: str):
        parse = self.morph.parse(raw_term)
        if not parse:
            return {}
        term = parse[0].normal_form
        return self.term2coord.get(term, {})

    def finalize(self):
        self.idf_cache = {}
        for term, posting in self.term2coord.items():
            df = len(posting)
            self.idf_cache[term] = math.log((1 + self.doc_count) / (1 + df)) + 1

        for term in self.term2coord:
            if term not in self.term2coord:
                self.term2coord[term] = len(self.term2coord)

    def save(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'docs': self.docs,
                'term2coord': self.term2coord,
                'doc_term_freqs': self.doc_term_freqs,
                'idf_cache': self.idf_cache,
                'index': self.index,
                'title_index': self.title_index
            }, f, ensure_ascii=False)

    def load(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.docs = data['docs']
            self.term2coord = data['term2coord']
            self.doc_term_freqs = data['doc_term_freqs']
            self.idf_cache = data['idf_cache']
            self.index = data['index']
            self.title_index = data['title_index']
            self.doc_count = len(self.docs)

    def vectorize(self, tokens: list[str]) -> np.ndarray:
        vec = np.zeros(len(self.term2coord))
        term_list = list(self.term2coord.keys())
        for token in tokens:
            parse = self.morph.parse(token)
            if not parse:
                continue
            norm_token = parse[0].normal_form
            if norm_token in self.term2coord:
                idx = term_list.index(norm_token)
                tf = tokens.count(token) / len(tokens)
                idf = self.idf_cache.get(norm_token, 0)
                vec[idx] = tf * idf
        return vec

    def tfidf(self, doc_no: int) -> np.ndarray:
        vec = np.zeros(len(self.term2coord))
        term_list = list(self.term2coord.keys())
        tf_map = self.doc_term_freqs[doc_no]
        total_terms = sum(tf_map.values())
        for i, term in enumerate(term_list):
            tf = tf_map.get(term, 0) / total_terms if total_terms else 0
            idf = self.idf_cache.get(term, 0)
            vec[i] = tf * idf
        return vec

    def get_score(self, query_vec: np.ndarray, doc_no: int) -> float:
        doc_vec = self.tfidf(doc_no)
        numerator = np.dot(query_vec, doc_vec)
        denominator = np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        if denominator == 0:
            return 0.0
        return numerator / denominator
