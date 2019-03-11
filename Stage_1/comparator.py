import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import precision_score, recall_score, f1_score
from collections import OrderedDict
import features_code
import random

import warnings
warnings.filterwarnings("ignore")

features_code.generate_feature_csv('training_set')

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
        x_dev.append(row[:-1])
        y_dev.append(row[-1])

c = list(zip(x_dev, y_dev))
random.shuffle(c)
x_dev, y_dev = zip(*c)

print(len(x_dev))

# cross validation of all models
precisions = []
recalls = []
f1s = []
models = OrderedDict({
    'decision_tree': DecisionTreeClassifier,
    'random_forest': RandomForestClassifier,
    'svm': svm.SVC,
    'linear_reg': LinearRegression,
    'logistic_reg': LogisticRegression
})
for k, v in models.items():
    print('Running ' + k)
    if k != 'linear_reg':
        if k == 'svm':
            max_iter = 500
            precisions.append(np.mean(cross_val_score(v(max_iter=max_iter), x_dev, y_dev, scoring='precision_macro', cv=5)))
            recalls.append(np.mean(cross_val_score(v(max_iter=max_iter), x_dev, y_dev, scoring='recall_macro', cv=5)))
            f1s.append(np.mean(cross_val_score(v(max_iter=max_iter), x_dev, y_dev, scoring='f1_macro', cv=5)))
        else:
            precisions.append(np.mean(cross_val_score(v(), x_dev, y_dev, scoring='precision_macro', cv=5)))
            recalls.append(np.mean(cross_val_score(v(), x_dev, y_dev, scoring='recall_macro', cv=5)))
            f1s.append(np.mean(cross_val_score(v(), x_dev, y_dev, scoring='f1_macro', cv=5)))

    else:
        kf = KFold(n_splits=5)
        temp_precisions = []
        temp_recalls = []
        temp_f1s = []
        for train_index, test_index in kf.split(x_dev):
            x_temp_train, x_temp_test = np.array(x_dev)[train_index], np.array(x_dev)[test_index]
            y_temp_train, y_temp_test = np.array(y_dev)[train_index], np.array(y_dev)[test_index]
            clf = v().fit(x_temp_train, y_temp_train)
            preds = clf.predict(x_temp_test)
            thresh = 0.2
            temp_precisions.append(precision_score(y_temp_test, [1 if x > thresh else 0 for x in preds]))
            temp_recalls.append(recall_score(y_temp_test, [1 if x > thresh else 0 for x in preds]))
            temp_recalls.append(f1_score(y_temp_test, [1 if x > thresh else 0 for x in preds]))
        precisions.append(np.mean(temp_precisions))
        recalls.append(np.mean(temp_recalls))
        f1s.append(np.mean(temp_f1s))

    print(precisions[-1])
    print(recalls[-1])
    print(f1s[-1])

# output
for i in range(len(models)):
    print(list(models.keys())[i] + ' ::: ' + str(precisions[i]) + ' : ' + str(recalls[i]) + ' : ' + str(f1s[i]))

# graphs
