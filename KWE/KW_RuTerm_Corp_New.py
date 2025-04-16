import os
import re
import pandas as pd
from rutermextract import TermExtractor

base_folder = '/Users/juliak/Downloads/IMS2013-20242'
term_extractor = TermExtractor()
top_n = 10
results = []
index_counter = 1

def is_valid_term(term):
    # Проверим: только кириллические буквы и каждое слово ≥ 4 символов
    words = term.split()
    return (
        all(len(word) >= 4 for word in words) and
        all(re.fullmatch(r'[а-яА-ЯёЁ-]+', word) for word in words)
    )

for year_folder in os.listdir(base_folder):
    year_path = os.path.join(base_folder, year_folder)

    if os.path.isdir(year_path):
        for filename in os.listdir(year_path):
            file_path = os.path.join(year_path, filename)

            if (
                os.path.isfile(file_path) and
                filename.endswith(".txt") and
                "Abstract" not in filename and
                "KW" not in filename
            ):
                parts = filename.split("_")

                try:
                    ims_index = parts.index("IMS")
                    author = "_".join(parts[:ims_index])
                    year_part = parts[ims_index + 1]
                    year = ''.join(filter(str.isdigit, year_part))
                except (ValueError, IndexError):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                except Exception:
                    text = ""

                try:
                    all_terms = term_extractor(text)
                    filtered = [
                        term.normalized
                        for term in all_terms
                        if is_valid_term(term.normalized)
                    ]

                    # Убираем дубликаты
                    seen = set()
                    final_terms = []
                    for term in filtered:
                        if term not in seen:
                            seen.add(term)
                            final_terms.append(term)
                        if len(final_terms) == top_n:
                            break

                    kw_string = ", ".join(final_terms)
                except Exception:
                    kw_string = ""

                results.append({
                    "Index": index_counter,
                    "Year": year,
                    "Name": author,
                    "KW": kw_string
                })

                index_counter += 1

if results:
    df = pd.DataFrame(results)
    df.to_csv("RuTerm_New_Corp.csv.csv", index=False)
