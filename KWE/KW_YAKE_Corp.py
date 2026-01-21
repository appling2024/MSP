import os
import pandas as pd
import yake

base_folder = '/Users/juliak/Downloads/IMS2013-20242'

# Создаём два экстрактора для n=1 и n=2
kw_extractor_1 = yake.KeywordExtractor(lan="ru", n=1, top=20)
kw_extractor_2 = yake.KeywordExtractor(lan="ru", n=2, top=20)

results = []
index_counter = 1
top_n = 10

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

                # Извлекаем ключевые выражения с n=1 и n=2
                try:
                    kw_1 = kw_extractor_1.extract_keywords(text)
                    kw_2 = kw_extractor_2.extract_keywords(text)

                    # Объединяем, убираем дубликаты, сортируем по score
                    combined = kw_1 + kw_2
                    unique_kw = {}
                    for kw, score in combined:
                        if kw not in unique_kw or score < unique_kw[kw]:
                            unique_kw[kw] = score

                    sorted_kw = sorted(unique_kw.items(), key=lambda x: x[1])
                    top_keywords = [kw for kw, _ in sorted_kw[:top_n]]
                    kw_string = ", ".join(top_keywords)
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
    df.to_csv("YAKE_Corp.csv", index=False)
