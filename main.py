import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score

import warnings
warnings.filterwarnings("ignore")

# read from file
x_dev = []
y_dev = []
with open('features.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = True
    for row in reader:
        if header:
            header = False
            continue
        row = [int(x) for x in row[1:]]
        x_dev.append(row[1:-1])
        y_dev.append(row[-1])

# cross validation of all models
precisions = []
recalls = []
models = [
    DecisionTreeClassifier,
    RandomForestClassifier,
    svm.SVC,
    #LinearRegression,
    LogisticRegression
]

for model in models:
    print(model)
    precisions.append(np.mean(cross_val_score(model(), x_dev, y_dev, scoring='precision_macro', cv=5)))
    recalls.append(np.mean(cross_val_score(model(), x_dev, y_dev, scoring='recall_macro', cv=5)))

# output
print(precisions)
print(recalls)

# graphs