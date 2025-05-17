import json
from pymorphy2 import MorphAnalyzer
import math

class Index:
	def __init__(self):
		self.index = {}
		self.title_index = {}
		self.docs = []
		self.term2coord = {}
		self.morph = MorphAnalyzer()
	
	def add_doc(self, doc_name: str) -> int:
		self.docs.append(doc_name)
		return len(self.docs) - 1

	def add(self, doc_no: int, raw_term: str, pos: int, is_title: bool) -> None:
		parse = self.morph.parse(raw_term)
		if parse:
			term = parse[0].normal_form
			if is_title:
				if term not in self.title_index:
					self.title_index[term] = {}
				if doc_no not in self.title_index[term]:
					self.title_index[term][doc_no] = []
				self.title_index[term][doc_no].append(pos)
			else:
				if term not in self.index:
					self.index[term] = {}
				if doc_no not in self.index[term]:
					self.index[term][doc_no] = []
				self.index[term][doc_no].append(pos)

	def get(self, raw_term: str) -> dict[int, list[int]]:
		parse = self.morph.parse(raw_term)
		if parse:
			term = parse[0].normal_form
			return self.index.get(term, {})
		return {}

	def get_in_title(self, raw_term: str) -> dict[int, list[int]]:
		parse = self.morph.parse(raw_term)
		if parse:
			term = parse[0].normal_form
			return self.title_index.get(term, {})
		return {}
	
	def tfidf(self, term: str, tf: int) -> float:
		tf_log = 1 + math.log(tf)
		df = 1
		idf = math.log(len(self.docs) / df)
		return tf_log * idf

	def vectorize(self, terms: list[str]) -> list[float]:
		space_size = len(self.term2coord)  # Определяет размер векторного пространства (количество уникальных терминов)
		tfs = {}
		for term in terms:
			if term not in tfs:
				tfs[term] = 0
			tfs[term] += 1
		v = [0] * space_size  # Создает нулевой вектор размером space_size
		for term in tfs:
			if term not in self.term2coord:
				continue
			v[self.term2coord[term]] = self.tfidf(term, tfs[term])  
		return v  # Возвращает бинарный вектор документа
	
	def get_score(self, Q: list[float], doc_no: int) -> float:
		terms = [term for term, posting in self.index.items() if doc_no in posting]  # Получает все термины, встречающиеся в документе
		D = self.vectorize(terms)  # Преобразует термины документа в вектор
		score = 0  # Инициализирует счетчик релевантности
		return score  # Возвращает текущий счетчик (пока всегда 0)
		# calc cos  # TODO: нужно реализовать расчет косинусного сходства между вектором запроса Q и вектором документа D

	def finalize(self):
		for term in self.index:
			self.term2coord[term] = len(self.term2coord)

	def save(self, fname: str):
		with open(fname, 'w') as fh:
			json.dump({
				'index': self.index,
				'title_index': self.title_index,
				'docs': self.docs,
				'term2coord': self.term2coord,
			}, fh)

	def load(self, fname: str):
		with open(fname) as fh:
			temp = json.load(fh)
			self.index, self.title_index, self.docs, self.term2coord =\
				 temp['index'], temp['title_index'], temp['docs'], temp['term2coord']

	def get_normalized_terms(self, term: str) -> list[str]:
		parsed = self.morph.parse(term)
		return [p.normal_form for p in parsed]