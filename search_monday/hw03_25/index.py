# Импорт необходимых библиотек
import math  # для математических операций
import json  # для работы с JSON файлами
import numpy as np  # для векторных операций
from pymorphy2 import MorphAnalyzer  # для морфологического анализа русского языка

class Index:
    def __init__(self):
        # Инициализация основных структур данных
        self.index = {}  # Основной инвертированный индекс для текста
        self.title_index = {}  # Отдельный индекс для заголовков
        self.docs = []  # Список путей к документам
        self.term2coord = {}  # Словарь: термин -> {doc_id -> [позиции в документе]}
        self.doc_term_freqs = []  # Список словарей частот терминов для каждого документа
        self.doc_count = 0  # Счетчик документов
        self.morph = MorphAnalyzer()  # Инициализация морфологического анализатора

    def add_doc(self, path: str) -> int:
        # Добавление нового документа в индекс
        self.docs.append(path)  # Сохраняем путь к документу
        self.doc_term_freqs.append({})  # Создаем пустой словарь частот для нового документа
        self.doc_count += 1  # Увеличиваем счетчик документов
        return self.doc_count - 1  # Возвращаем ID документа (индекс в списке)

    def add(self, doc_no: int, raw_term: str, pos: int, is_title: bool):
        # Добавление термина в индекс
        parse = self.morph.parse(raw_term)  # Морфологический анализ термина
        if not parse:  # Если анализ не удался, пропускаем
            return
        term = parse[0].normal_form  # Получаем нормальную форму слова

        # Добавляем позицию в term2coord
        if term not in self.term2coord:  # Если термин встречается впервые
            self.term2coord[term] = {}  # Создаем словарь для документа
        if doc_no not in self.term2coord[term]:  # Если документ встречается впервые для термина
            self.term2coord[term][doc_no] = []  # Создаем список позиций
        self.term2coord[term][doc_no].append(pos)  # Добавляем позицию

        # Обновляем частоты терминов в документе
        tf_map = self.doc_term_freqs[doc_no]  # Получаем словарь частот документа
        tf_map[term] = tf_map.get(term, 0) + 1  # Увеличиваем частоту термина

        # Добавляем в соответствующий индекс (основной или заголовков)
        index_target = self.title_index if is_title else self.index  # Выбираем целевой индекс
        if term not in index_target:  # Если термин встречается впервые
            index_target[term] = {}  # Создаем словарь для документа
        if doc_no not in index_target[term]:  # Если документ встречается впервые для термина
            index_target[term][doc_no] = []  # Создаем список позиций
        index_target[term][doc_no].append(pos)  # Добавляем позицию

    def get(self, raw_term: str):
        # Получение постингов для термина
        parse = self.morph.parse(raw_term)  # Морфологический анализ
        if not parse:  # Если анализ не удался
            return {}  # Возвращаем пустой словарь
        term = parse[0].normal_form  # Получаем нормальную форму
        return self.term2coord.get(term, {})  # Возвращаем постинги или пустой словарь

    def finalize(self):
        # Финальная обработка индекса
        self.idf_cache = {}  # Создаем кэш для IDF значений
        for term, posting in self.term2coord.items():  # Для каждого термина
            df = len(posting)  # Количество документов с термином
            # Вычисляем IDF с сглаживанием
            self.idf_cache[term] = math.log((1 + self.doc_count) / (1 + df)) + 1

        # Создаем отображение терминов в индексы
        for term in self.term2coord:
            if term not in self.term2coord:
                self.term2coord[term] = len(self.term2coord)

    def save(self, path: str):
        # Сохранение индекса в JSON файл
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'docs': self.docs,  # Пути к документам
                'term2coord': self.term2coord,  # Термины и их позиции
                'doc_term_freqs': self.doc_term_freqs,  # Частоты терминов
                'idf_cache': self.idf_cache,  # Кэш IDF значений
                'index': self.index,  # Основной индекс
                'title_index': self.title_index  # Индекс заголовков
            }, f, ensure_ascii=False)  # Сохраняем с поддержкой Unicode

    def load(self, path: str):
        # Загрузка индекса из JSON файла
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Загружаем данные
            self.docs = data['docs']  # Восстанавливаем пути
            self.term2coord = data['term2coord']  # Восстанавливаем термины и позиции
            self.doc_term_freqs = data['doc_term_freqs']  # Восстанавливаем частоты
            self.idf_cache = data['idf_cache']  # Восстанавливаем IDF кэш
            self.index = data['index']  # Восстанавливаем основной индекс
            self.title_index = data['title_index']  # Восстанавливаем индекс заголовков
            self.doc_count = len(self.docs)  # Обновляем счетчик документов

    def vectorize(self, tokens: list[str]) -> np.ndarray:
        # Создание TF-IDF вектора для списка токенов
        vec = np.zeros(len(self.term2coord))  # Создаем нулевой вектор
        term_list = list(self.term2coord.keys())  # Получаем список всех терминов
        for token in tokens:  # Для каждого токена
            parse = self.morph.parse(token)  # Морфологический анализ
            if not parse:  # Если анализ не удался
                continue  # Пропускаем токен
            norm_token = parse[0].normal_form  # Получаем нормальную форму
            if norm_token in self.term2coord:  # Если термин есть в индексе
                idx = term_list.index(norm_token)  # Получаем индекс термина
                tf = tokens.count(token) / len(tokens)  # Вычисляем TF
                idf = self.idf_cache.get(norm_token, 0)  # Получаем IDF
                vec[idx] = tf * idf  # Вычисляем TF-IDF
        return vec  # Возвращаем вектор

    def tfidf(self, doc_no: int) -> np.ndarray:
        # Создание TF-IDF вектора для документа
        vec = np.zeros(len(self.term2coord))  # Создаем нулевой вектор
        term_list = list(self.term2coord.keys())  # Получаем список всех терминов
        tf_map = self.doc_term_freqs[doc_no]  # Получаем частоты терминов документа
        total_terms = sum(tf_map.values())  # Общее количество терминов
        for i, term in enumerate(term_list):  # Для каждого термина
            # Вычисляем TF с учетом общего количества терминов
            tf = tf_map.get(term, 0) / total_terms if total_terms else 0
            idf = self.idf_cache.get(term, 0)  # Получаем IDF
            vec[i] = tf * idf  # Вычисляем TF-IDF
        return vec  # Возвращаем вектор

    def get_score(self, query_vec: np.ndarray, doc_no: int) -> float:
        # Вычисление косинусного сходства между запросом и документом
        doc_vec = self.tfidf(doc_no)  # Получаем вектор документа
        numerator = np.dot(query_vec, doc_vec)  # Скалярное произведение
        denominator = np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)  # Произведение норм
        if denominator == 0:  # Если знаменатель равен нулю
            return 0.0  # Возвращаем нулевое сходство
        return numerator / denominator  # Возвращаем косинусное сходство
