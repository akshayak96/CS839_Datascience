import os
import re
import csv
import vectorizer

def to_feature_vector(phrase, before_phrase, after_phrase, positive_examples):
    #print(before_phrase, phrase, after_phrase)
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
    vectorizer_features = vectorizer.vectorize_phrase(before_phrase, phrase.split(" "), after_phrase)
    feature_vector['text'] = final_phrase
    feature_vector['name'] = int(name)
    _VECTORIZER_ = vectorizer._VECTORIZER_NAMES_

    for f in range(len(_VECTORIZER_)):
        feature_vector[_VECTORIZER_[f]] = int(vectorizer_features[f])
        
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
    markup_path = os.path.join(current_path, 'training_set')
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
                if len(name) > 1 and name.lower().replace(".", "") != "jr" and \
                        name.lower().replace(".", "") != "sr" and \
                        name.lower().replace(".", "") != "ii" and \
                        name.lower().replace(".", "") != "iii" and \
                        name.lower().replace(".", "") != "iv":
                            tagged_names.append(name)
            #print(matches)
            clean_text = modified_text.replace("<n>", "").replace("<\\n>", "").replace("</n>", "").replace("\ufeff", "")
            backlog_1_back = None
            backlog_2_back = None
            backlog_3_back = None
            backlog_4_back = None
            backlog_5_back = None
            backlog_6_back = None
            clean_text_list = clean_text.split(" ")
            clean_text_list = list(filter(("").__ne__, clean_text_list))
            for i in clean_text_list:
                if i == "":
                    print ("oh no")
            feature_vectors = []
            for word_index in range(len(clean_text_list)):
                word = clean_text_list[word_index]
                after_phrase = []
                try: 
                    look_ahead_1 = clean_text_list[word_index + 1]
                except:
                    look_ahead_1 = None
                try:
                    look_ahead_2 = clean_text_list[word_index + 2]
                except:
                    look_ahead_2 = None
                try:
                    look_ahead_3 = clean_text_list[word_index + 3]
                except:
                    look_ahead_3 = None
                if look_ahead_1:
                    after_phrase.append(look_ahead_1)
                if look_ahead_2:
                    after_phrase.append(look_ahead_2)
                if look_ahead_3:
                    after_phrase.append(look_ahead_3)
                #length 1 word
                before_phrase = []
                if backlog_3_back:
                    before_phrase.append(backlog_3_back)
                if backlog_2_back:
                    before_phrase.append(backlog_2_back)
                if backlog_1_back:
                    before_phrase.append(backlog_1_back)
                feature_vec = to_feature_vector(word, before_phrase, after_phrase, tagged_names)
                feature_vectors.append(feature_vec)
                #length 2 word
                if(backlog_1_back != None):
                    before_phrase = []
                    if backlog_4_back:
                        before_phrase.append(backlog_4_back)
                    if backlog_3_back:
                        before_phrase.append(backlog_3_back)
                    if backlog_2_back:
                        before_phrase.append(backlog_2_back)
                    length_2_word = backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_2_word, before_phrase, after_phrase, tagged_names)
                    feature_vectors.append(feature_vec)
                #length 3 word
                if(backlog_2_back != None):
                    before_phrase = []
                    if backlog_5_back:
                        before_phrase.append(backlog_5_back)
                    if backlog_4_back:
                        before_phrase.append(backlog_4_back)
                    if backlog_3_back:
                        before_phrase.append(backlog_3_back)
                    length_3_word = backlog_2_back + " " + backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_3_word, before_phrase, after_phrase, tagged_names)
                    feature_vectors.append(feature_vec)
                #length 4 word
                """
                if(backlog_3_back != None):
                    before_phrase = []
                    if backlog_6_back:
                        before_phrase.append(backlog_6_back)
                    if backlog_5_back:
                        before_phrase.append(backlog_5_back)
                    if backlog_4_back:
                        before_phrase.append(backlog_4_back)
                    length_4_word = backlog_3_back + " " + backlog_2_back + " " + backlog_1_back + " " + word
                    feature_vec = to_feature_vector(length_4_word, before_phrase, after_phrase, tagged_names)
                    feature_vectors.append(feature_vec)
                """
                #bookKeeping
                backlog_6_back = backlog_5_back
                backlog_5_back = backlog_4_back
                backlog_4_back = backlog_3_back
                backlog_3_back = backlog_2_back
                backlog_2_back = backlog_1_back
                backlog_1_back = word
            #    if backlog_1_back
            #for feature in feature_vectors:
            #    if(feature[1] == True):
            #        print(feature)
            for feature in feature_vectors:
                #if(good_feature(feature)):
                feature_vector_complete.append(feature)
                    #print(feature)

    with open('features.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['text'] + vectorizer._VECTORIZER_NAMES_ + ['name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for feature in feature_vector_complete:
            writer.writerow(feature)
  
if __name__== "__main__":
  generate_feature_csv()