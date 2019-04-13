import os
import codecs
import re
import csv


def main():
    full_data = []

    directory = "../data/metacritic_html_data"
    all_files = os.listdir(directory)
    path_files = []
    for file in all_files:
        if file.endswith(".html"):
            path_files.append(os.path.join(directory, file))

    for file_name in path_files:
        f = codecs.open(file_name, 'r', 'utf-8')
        data = "".join(list(f))


        regex_match = "<table class=\"clamp-list\">"
        matches = re.search(regex_match, data)
        first_cut = matches.start()

        data_first = data[first_cut:]

        regex_match_end = "<div class=\"marg_top1\">"
        matches_end = re.search(regex_match_end, data_first)
        end_cut = matches_end.end()

        data_second = data_first[:end_cut]

        data_final = data_second.replace("\n", "")
        data_final = data_final.replace("<div class=\"metascore_w user large movie tbd\">","<div class=\"metascore_w user large movie positive\">")
        data_final = data_final.replace("<div class=\"metascore_w user large movie mixed\">","<div class=\"metascore_w user large movie positive\">")
        data_final = data_final.replace("<div class=\"metascore_w user large movie negative\">","<div class=\"metascore_w user large movie positive\">")
        data_final = data_final.replace("<div class=\"metascore_w large movie positive perfect\">","<div class=\"metascore_w large movie positive\">")

        regex_match_title = "(?<=<h3>)(.*?)(?=</h3>)"
        matches_title = re.findall(regex_match_title, data_final)
        matches_title = list(matches_title)

        regex_match_summary = "(?<=<div class=\"summary\">)(.*?)(?=</div>)"
        matches_summary = re.findall(regex_match_summary, data_final)
        matches_summary = list(matches_summary)

        regex_match_release = "(?<=<span class=\"label\">Release Date:</span><span>)(.*?)(?=</span>)"
        matches_release = re.findall(regex_match_release, re.sub(r'</span>\s*<span>', r'</span><span>', data_final))
        matches_release = list(matches_release)

        regex_match_meta_rating = "(?<=<div class=\"metascore_w large movie positive\">)(.*?)(?=</div>)"
        matches_meta_rating = re.findall(regex_match_meta_rating, data_final)
        matches_meta_rating = list(matches_meta_rating)[::2]

        regex_match_user_rating = "(?<=<div class=\"metascore_w user large movie positive\">)(.*?)(?=</div>)"
        matches_user_rating = re.findall(regex_match_user_rating, data_final)
        matches_user_rating = list(matches_user_rating)

        for index in range(len(matches_title)):
            new_movie = {}
            new_movie['title'] = matches_title[index].strip('"')
            if matches_release[index] != "TBA":
               matches_release[index] = matches_release[index].split(', ')[1]
            new_movie['release_year'] = matches_release[index]
           # new_movie['meta_rating'] = matches_meta_rating[index]
            new_movie['movie_rating'] = matches_user_rating[index]
            new_movie['summary'] = matches_summary[index].strip().strip('"')
            full_data.append(new_movie)

    with open('../data/metacritic.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'release_year',
                      #'meta_rating',
                      'movie_rating','summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in full_data:
            writer.writerow(row)


if __name__== "__main__":
    main()
