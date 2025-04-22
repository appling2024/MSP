import os
import csv



def extract_russian_keywords(root_folder):
    keywords_dict = {}

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('_KW_rus.txt'):
                file_path = os.path.join(root, file)
                article_id = '_'.join(file.split('_')[:3])

                with open(file_path, 'r', encoding = 'utf-8') as f:
                    content = f.read().strip()
                    keywords = [kw.strip().lower() for kw in content.replace(';', ',').split(',') if kw.strip()]
                    keywords_dict[article_id] = keywords

    return keywords_dict

file_path = r"C:\Users\yes\Desktop\Python\Keywords\IMS2013-2024"
keywords = extract_russian_keywords(file_path)



def load_generated_keywords(csv_path):
    generated_dict =  {}

    with open(csv_path, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            filename = row[0].strip()
            if filename.endswith("_rus.txt"):
                article_id = '_'.join(filename.split('_')[:3])
                all_keywords = row[-1].strip()
                keywords = [kw.strip().lower() for kw in all_keywords.split(',') if kw.strip()]
                generated_dict[article_id] = keywords

    return generated_dict

csv_path = r"C:\Users\yes\Desktop\Python\Keywords\keywords_abstracts.csv"
generated_keywords = load_generated_keywords(csv_path)



def compare_keywords(generated, reference):
    comparison_results = []
    for article_id, gen_keywords in generated.items():
        ref_keywords = reference.get(article_id, [])
        matches = set(gen_keywords) & set(ref_keywords)
        match_percent = round(len(matches) / len(ref_keywords) * 100, 2) if ref_keywords else 0.0
        comparison_results.append({
            'Article ID': article_id,
            'Generated keywords':','.join(gen_keywords),
            'Reference keywords':','.join(ref_keywords),
            'Matches':','.join(matches),
            'Match %': match_percent
        })

    return comparison_results

comparison_results = compare_keywords(generated_keywords, keywords)

for result in comparison_results[:5]:
    print("Article ID:", result['Article ID'])
    print("Generated Keywords:", result['Generated keywords'])
    print("Reference Keywords:", result['Reference keywords'])
    print("Matches:", result['Matches'])
    print("Match %:", result['Match %'])

def save_to_csv(results, output_path):
    with open(output_path, 'w', newline = '', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = ['Article ID', 'Generated keywords', 'Reference keywords', 'Matches', 'Match %'])
        writer.writeheader()
        writer.writerows(results)

output_csv_path = r"C:\Users\yes\Desktop\Python\Keywords\comparison_results.csv"
save_to_csv(comparison_results, output_csv_path)
