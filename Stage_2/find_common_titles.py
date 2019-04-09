import os
import codecs
import re
import csv

index = 0 #to index imdb.csv
index2 = 0 #to index metacritic.csv
title = [None]*3500  #stores the titles of imdb.csv
title2 = [None]*3500 #stores the titles of metacritic.csv
title3 = [None]*1000 #stores the common titles from the 2 web sources

with open('imdb.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        title[index] = row[0]
       # print(title[index])
        index = index + 1
#print("First file movies")

with open('metacritic.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        title2[index2] = row[0]
        #print(title2[index2])
        index2 = index2 + 1
#print("Second file movies")

i = 0    #index that traverses imdb.csv
k = 0    #index of title3
while(i<index):
    j = 0  #index that traverses metacritic.csv
    #print("Index:")
    #print(i)
    while(j<index2):
       # print(j)
        if(title[i]==title2[j]):
            title3[k] = title[i]
            k = k + 1
        j = j+1
    i = i+1

        #else:
            #print("Unequal")
    #print("Index:"+i)
#for index in range(len(title3)):
 #   print(title3[index])
print("Total common titles")
print(k-1)
final = 0  #index to write the common titles into a csv

with open('string.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    while(final<k):
        print("Writing....")
        print(final)
        #title3[final] = title3[final].encode('utf-8')
        writer.writerow([title3[final]])
        final = final + 1
csvFile.close()
