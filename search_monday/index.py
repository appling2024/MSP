import json
from pymorphy2 import MorphAnalyzer


class Index:
	def __init__(self):
		self.index = {}
		self.title_index = {}
		self.docs = []
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

	def save(self, fname: str):
		with open(fname, 'w') as fh:
			json.dump({
				'index': self.index,
				'title_index': self.title_index,
				'docs': self.docs,
			}, fh)

	def load(self, fname: str):
		with open(fname) as fh:
			temp = json.load(fh)
			self.index, self.title_index, self.docs =\
				 temp['index'], temp['title_index'], temp['docs']

	def get_normalized_terms(self, term: str) -> list[str]:
		parsed = self.morph.parse(term)
		return [p.normal_form for p in parsed]