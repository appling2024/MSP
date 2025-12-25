# Retrieval-Augmented Generation (RAG)

Минимальная реализация RAG-пайплайна:
- retrieval на sentence-transformers
- генерация ответов с помощью T5
- оценка semantic similarity

## Запуск
```bash
pip install -r requirements.txt
python ingest.py
python main.py
