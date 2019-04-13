import os
import csv
from nltk import ngrams
import re
from Stage_1 import vectorizer
import numpy as np

def is_alnum(c):
    return c.isalnum() or c == "'"

def gen(name):
    dir_name = name

    files = []
    if os.path.isdir(dir_name):
        for file_name in os.listdir(dir_name):
            files.append(os.path.join(dir_name, file_name))

    regrex = "(?<=<n>)(.*?)(?=<\\\\n>)"

    N = 3
    i = 0

    csvfile = open('features.csv', 'w', newline='', encoding="utf-8")
    writer = csv.writer(csvfile)

    lens = []
    for item in files:
        print(i)
        with open(item) as f:
            local_names = []
            try:
                corpus = " ".join(f.readlines())
                lens.append(len(corpus.split(" ")))
            except UnicodeDecodeError:
                continue
            matches = re.findall(regrex, corpus)
            matches = list(set(matches))
            for match in matches:
                if match not in local_names:
                    local_names.append(match)
                n = len(match.split(" "))
                for match_sub in match.split(" "):
                    if match_sub not in local_names:
                        local_names.append(match_sub)
                if n == 3:
                    local_names.append(match.split(" ")[1] + " " + match.split(" ")[2])

            for name in local_names:
                corpus = corpus.replace("<n>" + name + "<\\n>", name).replace("\"", "").replace(".", " . ").replace("?", " ? ").replace(",", " , ").replace(":", " : ")

            n = 1
            while n <= N:
                tokens = list(ngrams(corpus.split(), n + 2))
                for token in tokens:
                    if not all(is_alnum(c) for c in token[0]) or not all(is_alnum(c) for c in token[-1]):
                        continue
                    if not all(all(is_alnum(c) for c in w) for w in token[1:-1]):
                        continue
                    if vectorizer.capital_check([[], token[1:-1], []]) < 0:
                        continue
                    vec = vectorizer.vectorize_phrase(token[0], token[1:-1], token[-1])
                    writer.writerow([[token[0], " ".join(token[1:-1]), token[-1]]] + vec + [1 if " ".join(token[1:-1]) in local_names else 0])
                n += 1

        i += 1

    csvfile.close()
    print(np.mean(lens))

if __name__ == '__main__':
    gen('Stage_1/training_set')