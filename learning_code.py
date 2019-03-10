def main():
    feature_data = []
    classification = []
    with open('features.csv', 'r', encoding="utf-8") as csvfile:
        csv_data = csv.DictReader(csvfile)
        header = None
        for row in csv_data:
            row_data = []
            if header == None:
                header = list(row.keys())
                print (header)
            for key in header:
                if key == "text":
                    continue
                if key != "name":
                    try:    
                        row_data.append(int(row[key]))
                    except:
                        row_data.append(row[key])
                else:
                    classification.append(int(row[key]))

            feature_data.append(row_data)
            #print(header)
        #print (row)
        
    decision_tree = tree.DecisionTreeClassifier()
    decision_tree = decision_tree.fit(feature_data, classification)

if __name__== "__main__":
  main()