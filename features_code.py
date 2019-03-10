import os
import re
import csv

def to_feature_vector(phrase, past_word, positive_examples):
    feature_vector = {}
    to_remove = [".",",","\"","\'", "\'s"]
    final_phrase = phrase.strip()
    clean_phrase = phrase
    for bad in to_remove:
        if clean_phrase.endswith(bad):
            clean_phrase = clean_phrase[:len(clean_phrase)-len(bad)]
        #clean_phrase = clean_phrase.replace(bad, "")
    #print (clean_phrase)
    name = False
    if clean_phrase in positive_examples:
        name = True
    feature_vector['text'] = final_phrase
    feature_vector['name'] = int(name)
    feature_vector['possessive'] = int(phrase.endswith("\'s"))
    feature_vector['comma_follows'] = int(phrase.endswith(","))
    feature_vector['comma_in_middle'] = int("," in clean_phrase)
    return(feature_vector)

def good_feature(feature):
    #only consider strings with a single capital letter
    word = feature['text']
    all_words = word.split(" ")
    has_uppercase = any(letter.isupper() for letter in word)
    all_words_uppercase = True
    for ch in all_words:
        if len(ch) == 0:
            continue
        elif not ch[0].isupper():
            all_words_uppercase = False
            break
    return has_uppercase and all_words_uppercase

def generate_feature_csv():
    current_path = os.getcwd()
    markup_path = os.path.join(current_path, 'Markup_Files')
    markup_files_temp = os.listdir(markup_path)
    markup_files = []
    for file in markup_files_temp:
        markup_files.append(os.path.join(markup_path,file))    
    
    feature_vector_complete = []
    for file in markup_files:
        tagged_names = None
        with open(file, 'r', encoding="utf-8") as markup_file:
            full_text = markup_file.readlines()
            text = "".join(full_text)
            modified_text = text.replace("\n", " ")

            regrex = "(?<=<n>)(.*?)(?=<\\\\n>)"
            #print(re.findall("<n>([^]*)<\\\\n>", modified_text))
            #print(re.findall("<\\\\n>", modified_text))
            matches = re.findall(regrex, modified_text)
            matches = list(set(matches))
            for match in matches:
                breakdown = match.split(" ")
                if len(breakdown) == 2:
                    matches.append(breakdown[0])
                    matches.append(breakdown[1])
                if len(breakdown) == 3:
                    matches.append(breakdown[0])
                    matches.append(breakdown[1])
                    matches.append(breakdown[2])
                    matches.append(breakdown[0] + " " + breakdown[1])
                    matches.append(breakdown[1]+ " " + breakdown[2])
                if len(breakdown) == 4:
                    matches.append(breakdown[0])
                    matches.append(breakdown[1])
                    matches.append(breakdown[2])
                    matches.append(breakdown[3])
                    matches.append(breakdown[0] + " " + breakdown[1])
                    matches.append(breakdown[1]+ " " + breakdown[2])
                    matches.append(breakdown[2] + " " + breakdown[3])
                    matches.append(breakdown[0] + " " + breakdown[1] + " " + breakdown[2])
                    matches.append(breakdown[1] + " " + breakdown[2] + " " + breakdown[3])
                #print (breakdown)
            temp_names = list(set(matches))
            tagged_names = []
            for name in temp_names:
                if len(name) > 1:
                    tagged_names.append(name)
            #print(matches)
            clean_text = modified_text.replace("<n>", "").replace("<\\n>", "").replace("\ufeff", "")
            backlog_1_back = None
            backlog_2_back = None
            backlog_3_back = None
            backlog_4_back = None
            clean_text_list = clean_text.split(" ")
            clean_text_list = list(filter(("").__ne__, clean_text_list))
            for i in clean_text_list:
                if i == "":
                    print ("oh no")
            feature_vectors = []
            for word in clean_text_list:
                #length 1 word
                feature_vec = to_feature_vector(word, backlog_1_back, tagged_names)
                feature_vectors.append(feature_vec)
                #length 2 word
                if(backlog_1_back != None):
                    length_2_word = backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_2_word, backlog_2_back, tagged_names)
                    feature_vectors.append(feature_vec)
                #length 3 word
                if(backlog_2_back != None):
                    length_3_word = backlog_2_back + " " + backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_3_word, backlog_3_back, tagged_names)
                    feature_vectors.append(feature_vec)
                if(backlog_3_back != None):
                    length_4_word = backlog_3_back + " " + backlog_2_back + " " + backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_4_word, backlog_4_back, tagged_names)
                    feature_vectors.append(feature_vec)
                #bookKeeping
                backlog_4_back = backlog_3_back
                backlog_3_back = backlog_2_back
                backlog_2_back = backlog_1_back
                backlog_1_back = word
            #    if backlog_1_back
            #for feature in feature_vectors:
            #    if(feature[1] == True):
            #        print(feature)
            for feature in feature_vectors:
                if(good_feature(feature)):
                    feature_vector_complete.append(feature)
                    #print(feature)

    with open('features.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['text', 'possessive', 'comma_follows', 'comma_in_middle', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for feature in feature_vector_complete:
            writer.writerow(feature)
  
if __name__== "__main__":
  generate_feature_csv()