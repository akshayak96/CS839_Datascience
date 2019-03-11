import csv
from sklearn.tree import DecisionTreeClassifier
import features_code
from sklearn.metrics import precision_score, recall_score, f1_score

import warnings
warnings.filterwarnings("ignore")

features_code.generate_feature_csv('training_set')

# read from file
x_train = []
y_train = []
with open('features.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = True
    for row in reader:
        if header:
            header = False
            continue
        row = [int(x) for x in row[1:]]
        x_train.append(row[:-1])
        y_train.append(row[-1])

features_code.generate_feature_csv('test_set')
terms_test = []
x_test = []
y_test = []
with open('features.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = True
    for row in reader:
        if header:
            header = False
            continue
        terms_test.append(row[0])
        row = [int(x) for x in row[1:]]
        x_test.append(row[:-1])
        y_test.append(row[-1])

print(len(x_train))
print(len(x_test))
print(sum(y_train))
print(sum(y_test))


clf = DecisionTreeClassifier().fit(x_train, y_train)
preds = clf.predict(x_test)

print(len(preds))

for i in range(len(preds)):
    # print false positive
    if preds[i] != y_test[i] and preds[i] == 0:
        print(terms_test[i] + " : ", end='')
        print(x_test[i])

print("Precision : " + str(precision_score(y_pred=preds, y_true=y_test)))
print("Recall    : " + str(recall_score(y_pred=preds, y_true=y_test)))
print("F1        : " + str(f1_score(y_pred=preds, y_true=y_test)))

