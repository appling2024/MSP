import pprint

results = {'Иванова': {'Макулатура': 3, 'Металлолом': 1, 'Морковь': 4},
           'Петров': {'Макулатура': 10, 'Металлолом': 12, 'Морковь': 2},
           'Сидоров': {'Макулатура': 1, 'Металлолом': 1, 'Морковь': 3},
           'Алексеева': {'Макулатура': 1, 'Металлолом': 2, 'Морковь': 8},
           'Джонсон': {'Макулатура': 23, 'Металлолом': 5, 'Морковь': 2}}


#pprint.pprint(results['Петров']['Морковь'])

f = open('NewResults0.txt')

for line in f:
    items = line.split()
    name = items[0]
    collect = items[1]   
    weight = int(items[2])
    results[name][collect] += weight

f.close()

pprint.pprint(results)

