from index import Index  # Импорт класса Index из модуля index
import os  # Импорт модуля для работы с операционной системой


class Searcher:  # Класс для поиска по индексу
    def __init__(self, index_path: str, stopwords_path: str = None):  # Конструктор класса
        self.index = Index()  # Создание экземпляра класса Index
        self.index.load(index_path)  # Загрузка индекса из файла
        self.stopwords = set()  # Инициализация множества стоп-слов
        if stopwords_path:  # Если указан путь к файлу со стоп-словами
            with open(stopwords_path, 'r') as f:  # Открытие файла со стоп-словами
                self.stopwords = {word.strip().lower() for word in f if word.strip()}  # Загрузка стоп-слов в множество

    def search_and(self, terms: list[str]) -> list[tuple[str, float]]:  # Метод для поиска по И (AND)
        docs = set(self.index.get(terms[0]).keys())  # Получение множества документов с первым термином
        for term in terms[1:]:  # Для каждого следующего термина
            docs &= set(self.index.get(term).keys())  # Пересечение с множеством документов текущего термина
        result = []  # Инициализация списка результатов
        for doc_no in docs:  # Для каждого найденного документа
            relevance = sum(0.7 if self.index.get_in_title(term).get(doc_no) else 0.3  # Подсчет релевантности
                          if self.index.get(term).get(doc_no) else 0 for term in terms)  # 0.7 для заголовков, 0.3 для текста
            result.append((os.path.basename(doc_no), relevance))  # Добавление результата с релевантностью
        return sorted(result, key=lambda x: x[1], reverse=True)  # Сортировка по убыванию релевантности

    def search_or(self, terms: list[str]) -> list[tuple[str, float]]:  # Метод для поиска по ИЛИ (OR)
        docs = set()  # Инициализация пустого множества документов
        for term in terms:  # Для каждого термина
            docs.update(self.index.get(term).keys())  # Объединение множеств документов
        result = []  # Инициализация списка результатов
        for doc_no in docs:  # Для каждого найденного документа
            relevance = sum(0.7 if self.index.get_in_title(term).get(doc_no) else 0.3  # Подсчет релевантности
                          if self.index.get(term).get(doc_no) else 0 for term in terms)  # 0.7 для заголовков, 0.3 для текста
            result.append((os.path.basename(doc_no), relevance))  # Добавление результата с релевантностью
        return sorted(result, key=lambda x: x[1], reverse=True)  # Сортировка по убыванию релевантности

    def search_pos(self, terms: list[str], dist: int) -> list[str]:  # Метод для поиска по позиции
        assert len(terms) == 2  # Проверка, что запрос содержит ровно 2 термина
        result = []  # Инициализация списка результатов
        docs1 = self.index.get(terms[0])  # Получение документов с первым термином
        docs2 = self.index.get(terms[1])  # Получение документов со вторым термином
        for doc_no in set(docs1.keys()) & set(docs2.keys()):  # Для документов, содержащих оба термина
            pos1 = docs1[doc_no]  # Позиции первого термина
            pos2 = set(docs2[doc_no])  # Позиции второго термина
            for p in pos1:  # Для каждой позиции первого термина
                if dist > 0:  # Если расстояние положительное
                    if any((p + d) in pos2 for d in range(-dist, dist + 1) if d != 0):  # Проверка расстояния
                        result.append(os.path.basename(doc_no))  # Добавление документа в результаты
                        break  # Прерывание цикла
                else:  # Если расстояние отрицательное
                    if any(abs(p2 - p) >= abs(dist) for p2 in pos2):  # Проверка минимального расстояния
                        result.append(os.path.basename(doc_no))  # Добавление документа в результаты
                        break  # Прерывание цикла
        return result  # Возврат списка результатов

    def search_boolean(self, query: str) -> list[tuple[str, float]]:  # Метод для булевого поиска
        if not query:  # Если запрос пустой
            return []  # Возврат пустого списка
        tokens = query.split()  # Разбиение запроса на токены
        if len(tokens) == 1:  # Если запрос состоит из одного слова
            return [(os.path.basename(doc_no), 1.0)  # Возврат всех документов с этим словом
                   for doc_no in self.index.get(tokens[0]).keys()]
        if len(tokens) % 2 != 1:  # Проверка корректности формата запроса
            return []  # Возврат пустого списка при некорректном формате
        terms = tokens[::2]  # Получение терминов (каждый второй токен)
        op = tokens[1].lower()  # Получение оператора (второй токен)
        if op == "and":  # Если оператор AND
            return self.search_and(terms)  # Вызов поиска по И
        elif op == "or":  # Если оператор OR
            return self.search_or(terms)  # Вызов поиска по ИЛИ
        elif op.startswith('/'):  # Если оператор расстояния
            try:
                dist = int(op[1:])  # Получение значения расстояния
                return [(filename, 1.0) for filename in self.search_pos(terms, dist)]  # Поиск по позиции
            except ValueError:  # Если не удалось преобразовать в число
                return []  # Возврат пустого списка
        return []  # Возврат пустого списка для неизвестного оператора

    def search(self, query: str) -> list[int]:  # Метод для векторного поиска
        tokens = query.lower().split()  # Разбиение запроса на токены и приведение к нижнему регистру
        Q = self.index.vectorize(tokens)  # Векторизация запроса
        relev = {}  # Инициализация словаря релевантности
        for doc_no in self.index.docs:  # Для каждого документа
            score = self.index.get_score(Q, doc_no)  # Получение оценки релевантности
            relev[doc_no] = score  # Сохранение оценки
        return sorted(relev, key=relev.get, reverse=True)[:10]  # Возврат топ-10 документов


if __name__ == "__main__":  # Проверка, что скрипт запущен напрямую
    s = Searcher('index.inv', 'stopwords.txt')  # Создание экземпляра поисковика
    while True:  # Бесконечный цикл
        query = input("Enter query (or 'kill' to exit): ")  # Запрос поискового запроса
        if query.lower() == 'kill':  # Если введено 'kill'
            break  # Выход из цикла
        results = s.search(query)  # Выполнение поиска
        if results:  # Если есть результаты
            print(f"Found {len(results)} documents:")  # Вывод количества найденных документов
            for filename, relevance in results:  # Для каждого результата
                print(f"File {filename}: relevance {relevance}")  # Вывод имени файла и релевантности
        else:  # Если результатов нет
            print("No results found")  # Вывод сообщения об отсутствии результатов 