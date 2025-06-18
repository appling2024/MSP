import os  # Импорт модуля для работы с операционной системой
import os.path  # Импорт модуля для работы с путями файлов
from index import Index  # Импорт класса Index из модуля index


class Indexer:  # Класс для индексации документов
    def __init__(self, path: str):  # Конструктор класса, принимает путь к директории с документами
        self.index = Index()  # Создание экземпляра класса Index
        
        for fname in os.listdir(path):  # Перебор всех файлов в указанной директории
            if not fname.endswith('.txt'):  # Проверка, что файл имеет расширение .txt
                continue  # Пропуск файлов с другими расширениями
            fullpath = os.path.join(path, fname)  # Формирование полного пути к файлу
            doc_no = self.index.add_doc(fullpath)  # Добавление документа в индекс и получение его номера
            
            with open(fullpath, encoding="utf-8") as fh:  # Открытие файла с кодировкой UTF-8
                for pos, line in enumerate(fh):  # Перебор строк файла с их позициями
                    tokens = line.strip().lower().split()  # Разбиение строки на токены (слова)
                    for token_pos, token in enumerate(tokens):  # Перебор токенов с их позициями
                        self.index.add(doc_no, token, token_pos, is_title=(pos == 0))  # Добавление токена в индекс
        self.index.finalize()  # Завершение индексации
        self.index.save("index.inv")  # Сохранение индекса в файл


if __name__ == "__main__":  # Проверка, что скрипт запущен напрямую
    path = "small"  # Путь к директории с документами
    i = Indexer(path)  # Создание экземпляра индексатора и запуск индексации
