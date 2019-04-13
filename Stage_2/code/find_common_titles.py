import csv


imdb_titles = set()
with open('../data/imdb.csv', encoding='utf8') as imdb_file:
    reader = csv.DictReader(imdb_file)
    for row in reader:
        imdb_titles.add(row['title'])

common_titles = set()
with open('../data/metacritic.csv', encoding='utf8') as meta_file:
    reader = csv.DictReader(meta_file)
    for row in reader:
        if row['title'] in imdb_titles:
            common_titles.add(row['title'])

print(len(common_titles))
