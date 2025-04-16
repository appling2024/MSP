import os
import pandas as pd
from rutermextract import TermExtractor

base_folder = '/Users/juliak/Downloads/IMS2013-20242'
term_extractor = TermExtractor()
top_n = 10

results = []
index_counter = 1

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
                    terms = term_extractor(text)
                    keywords = [term.normalized for term in terms[:top_n]]
                    kw_string = ", ".join(keywords)
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
    df.to_csv("RuTerm_Corp.csv", index=False)


