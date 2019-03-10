import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score

# read from file
x_dev = []
y_dev = []
with open('features.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        x_dev.append(row[1:-1])
        y_dev.append(row[-1])

# cross validation of all models
precisions = []
recalls = []

for model in [DecisionTreeClassifier, RandomForestClassifier, svm.SVC, LinearRegression, LogisticRegression]:
    precisions.append(cross_val_score(model(), x_dev, y_dev, scoring='precision_macro', cv=5))
    recalls.append(cross_val_score(model(), x_dev, y_dev, scoring='precision_macro', cv=5))

# output
print(precisions)
print(recalls)

# graphs