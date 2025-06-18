import json  # Импорт модуля для работы с JSON файлами
from pymorphy2 import MorphAnalyzer  # Импорт морфологического анализатора для русского языка
import math  # Импорт модуля для математических операций

class Index:
	def __init__(self):
		self.index = {}  # Основной индекс для хранения терминов и их позиций в документах
		self.title_index = {}  # Индекс для хранения терминов, встречающихся в заголовках
		self.docs = []  # Список для хранения имен документов
		self.term2coord = {}  # Словарь для сопоставления терминов с координатами в векторном пространстве
		self.morph = MorphAnalyzer()  # Создание экземпляра морфологического анализатора
	
	def add_doc(self, doc_name: str) -> int:  # Метод для добавления нового документа
		self.docs.append(doc_name)  # Добавление имени документа в список
		return len(self.docs) - 1  # Возврат индекса добавленного документа

	def add(self, doc_no: int, raw_term: str, pos: int, is_title: bool) -> None:  # Метод для добавления термина в индекс
		parse = self.morph.parse(raw_term)  # Морфологический анализ термина
		if parse:  # Если анализ успешен
			term = parse[0].normal_form  # Получение нормальной формы термина
			if is_title:  # Если термин из заголовка
				if term not in self.title_index:  # Если термина нет в индексе заголовков
					self.title_index[term] = {}  # Создание записи для термина
				if doc_no not in self.title_index[term]:  # Если документа нет в записи термина
					self.title_index[term][doc_no] = []  # Создание списка позиций для документа
				self.title_index[term][doc_no].append(pos)  # Добавление позиции термина
			else:  # Если термин из основного текста
				if term not in self.index:  # Если термина нет в основном индексе
					self.index[term] = {}  # Создание записи для термина
				if doc_no not in self.index[term]:  # Если документа нет в записи термина
					self.index[term][doc_no] = []  # Создание списка позиций для документа
				self.index[term][doc_no].append(pos)  # Добавление позиции термина

	def get(self, raw_term: str) -> dict[int, list[int]]:  # Метод для поиска термина в основном индексе
		parse = self.morph.parse(raw_term)  # Морфологический анализ термина
		if parse:  # Если анализ успешен
			term = parse[0].normal_form  # Получение нормальной формы термина
			return self.index.get(term, {})  # Возврат словаря с позициями термина
		return {}  # Возврат пустого словаря, если анализ не удался

	def get_in_title(self, raw_term: str) -> dict[int, list[int]]:  # Метод для поиска термина в заголовках
		parse = self.morph.parse(raw_term)  # Морфологический анализ термина
		if parse:  # Если анализ успешен
			term = parse[0].normal_form  # Получение нормальной формы термина
			return self.title_index.get(term, {})  # Возврат словаря с позициями термина в заголовках
		return {}  # Возврат пустого словаря, если анализ не удался
	
	def tfidf(self, term: str, tf: int) -> float:  # Метод для вычисления TF-IDF
		tf_log = 1 + math.log(tf)  # Вычисление логарифмической частоты термина
		df = 1  # Количество документов, содержащих термин (пока фиксированное)
		idf = math.log(len(self.docs) / df)  # Вычисление обратной частоты документа
		return tf_log * idf  # Возврат произведения TF и IDF

	def vectorize(self, terms: list[str]) -> list[float]:  # Метод для векторизации документа
		space_size = len(self.term2coord)  # Определение размера векторного пространства
		tfs = {}  # Словарь для подсчета частоты терминов
		for term in terms:  # Для каждого термина в документе
			if term not in tfs:  # Если термина нет в словаре частот
				tfs[term] = 0  # Инициализация счетчика
			tfs[term] += 1  # Увеличение счетчика
		v = [0] * space_size  # Создание нулевого вектора
		for term in tfs:  # Для каждого термина
			if term not in self.term2coord:  # Если термина нет в отображении координат
				continue  # Пропуск термина
			v[self.term2coord[term]] = self.tfidf(term, tfs[term])  # Заполнение вектора TF-IDF значениями
		return v  # Возврат вектора документа
	
	def get_score(self, Q: list[float], doc_no: int) -> float:  # Метод для вычисления релевантности
		terms = [term for term, posting in self.index.items() if doc_no in posting]  # Получение терминов документа
		D = self.vectorize(terms)  # Векторизация документа
		score = 0  # Инициализация счетчика релевантности
		return score  # Возврат текущего счетчика (пока всегда 0)
		# calc cos  # TODO: нужно реализовать расчет косинусного сходства

	def finalize(self):  # Метод для финализации индекса
		for term in self.index:  # Для каждого термина в индексе
			self.term2coord[term] = len(self.term2coord)  # Назначение координаты в векторном пространстве

	def save(self, fname: str):  # Метод для сохранения индекса
		with open(fname, 'w') as fh:  # Открытие файла для записи
			json.dump({  # Сохранение данных в JSON
				'index': self.index,  # Основной индекс
				'title_index': self.title_index,  # Индекс заголовков
				'docs': self.docs,  # Список документов
				'term2coord': self.term2coord,  # Отображение терминов в координаты
			}, fh)

	def load(self, fname: str):  # Метод для загрузки индекса
		with open(fname) as fh:  # Открытие файла для чтения
			temp = json.load(fh)  # Загрузка данных из JSON
			self.index = temp['index']  # Загрузка основного индекса
			self.title_index = temp['title_index']  # Загрузка индекса заголовков
			self.docs = temp['docs']  # Загрузка списка документов
			self.term2coord = temp['term2coord']  # Загрузка отображения терминов в координаты

	def get_normalized_terms(self, term: str) -> list[str]:  # Метод для получения нормализованных форм
		parsed = self.morph.parse(term)  # Морфологический анализ термина
		return [p.normal_form for p in parsed]  # Возврат списка нормализованных форм