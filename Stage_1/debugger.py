import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from collections import OrderedDict
import random
import features_code

import warnings
warnings.filterwarnings("ignore")

features_code.generate_feature_csv('../training_set')

# read from file
terms = []
x_dev = []
y_dev = []
with open('features.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = True
    for row in reader:
        if header:
            print(row)
            header = False
            continue
        terms.append(row[0])
        row = [float(x) for x in row[1:]]
        x_dev.append(row[:-1])
        y_dev.append(row[-1])

c = list(zip(terms, x_dev, y_dev))
random.shuffle(c)
terms, x_dev, y_dev = zip(*c)

print(len(x_dev))

# cross validation of all models
precisions = []
recalls = []
f1s = []
models = OrderedDict({
    'ran_tree': RandomForestClassifier,
})
for k, v in models.items():
    print('Running ' + k)

    preds = cross_val_predict(v(), x_dev, y_dev, cv=5)

    for i in range(len(preds)):
        # print false positive
        if preds[i] != y_dev[i] and preds[i] == 1:
            print(terms[i] + " : ", end='')
            print(x_dev[i])

    print(np.mean(cross_val_score(v(), x_dev, y_dev, scoring='precision', cv=5)))
    print(np.mean(cross_val_score(v(), x_dev, y_dev, scoring='recall', cv=5)))
