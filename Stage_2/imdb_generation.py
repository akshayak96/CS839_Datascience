import os
import codecs
import re
import csv

# Fields : Movie name | Release Year | IMDB Score | <X Meta Score> | Runtime | <X Age Rating> | Categories | Summary | Votes | Gross

def main():
    full_data = []

    directory = "imbd_html_data"
    all_files = os.listdir(directory)
    path_files = []
    for file in all_files:
        if file.endswith(".html"):
            path_files.append(os.path.join(directory, file))
    # print(path_files)

    for file_name in path_files:
        f = codecs.open(file_name, 'r', 'utf-8')
        data = "".join(list(f))

        regrex = "<div id=\"pagecontent\" class=\"pagecontent\">"
        matches = re.search(regrex, data)
        first_cut = matches.start()

        data_first = data[first_cut:]

        regrex_end = "<script>"
        matches_end = re.search(regrex_end, data_first)
        end_cut = matches_end.start()

        data_second = data_first[:end_cut]

        data_final = data_second.replace("\n", "")
        data_final = re.sub(r"<a href=\"https://www.imdb.com/title/tt[0-9]+/\?ref_=adv_li_tt\">", r"<title>", data_final)
        data_final = re.sub(r"a href=\"https://www.imdb.com/name/nm[0-9]+/\?ref_=adv_li_dr_[0-9]+\">", r"<director>", data_final)
        data_final = re.sub(r"a href=\"https://www.imdb.com/name/nm[0-9]+/\?ref_=adv_li_st_[0-9]+\">", r"<star>", data_final)
        data_final = re.sub(r"<span class=\"text-muted\">Votes:</span>\s*<span name=\"nv\" data-value=\"[0-9]+\">", r"<votes>", data_final)
        data_final = re.sub(r"<span class=\"text-muted\">Gross:</span>\s*<span name=\"nv\" data-value=\"[0-9,]+\">", r"<gross>", data_final)
        data_final = re.sub(r"<span class=\"metascore\s*(favorable|mixed|unfavorable)\">", r"<metascore>", data_final)

        regrex_title = "<title>(.*?)</a>"
        matches_title = re.findall(regrex_title, data_final)
        matches_title = list(matches_title)

        regrex_release = "<span class=\"lister-item-year text-muted unbold\">\((.*?)\)</span>"
        matches_release_year = re.findall(regrex_release, data_final)
        matches_release_year = list(matches_release_year)

        regrex_imdb_score = "<score>(.*?)</strong>"
        matches_imdb_score = re.findall(regrex_imdb_score,
                                        re.sub(
                                            r"<span class=\"global-sprite rating-star imdb-rating\"></span>\s*<strong>",
                                            r"<score>",
                                            data_final
                                        )
                                        )
        matches_imdb_score = list(matches_imdb_score)

        # NOTE : not all movies have metascores, eg imbd_1 : Home Alone 2
        """
        regrex_meta_score = "<metascore>(.*?)</span>"
        matches_meta_score = re.findall(regrex_meta_score, data_final)
        matches_meta_score = [x.strip() for x in matches_meta_score]
        """

        regrex_runtime = "<span class=\"runtime\">(.*?)</span>"
        matches_runtime = re.findall(regrex_runtime, data_final)
        matches_runtime = list(matches_runtime)

        # NOTE : not all movies have age rating, eg imbd_11 : Mon Pere Ce Heros
        """
        regrex_age_rating = "<span class=\"certificate\">(.*?)</span>"
        matches_age_rating = re.findall(regrex_age_rating, data_final)
        matches_age_rating = list(matches_age_rating)

        if len(matches_age_rating) != len(matches_title):
            print(file_name)
        """

        regrex_cats = "<span class=\"genre\">(.*?)</span>"
        matches_cats = re.findall(regrex_cats, data_final)
        matches_cats = [x.strip() for x in matches_cats]

        regrex_summary = "<p class=\"text-muted\">(.*?)</p>"
        matches_summary = re.findall(regrex_summary, data_final)
        matches_summary = [x.strip() for x in matches_summary]

        regrex_votes = "<votes>(.*?)</span>"
        matches_votes = re.findall(regrex_votes, data_final)
        matches_votes = [x.strip() for x in matches_votes]

        regrex_gross = "<gross>(.*?)</span>"
        matches_gross = re.findall(regrex_gross, data_final)
        matches_gross = [x.strip() for x in matches_gross]

        for index in range(len(matches_title)):
            new_movie = {}
            new_movie['title'] = matches_title[index]
            new_movie['release_year'] = matches_release_year[index]
            new_movie['movie_rating'] = matches_imdb_score[index]
            #new_movie['meta_score'] = matches_meta_score[index]
           # new_movie['runtime'] = matches_runtime[index]
            #new_movie['age_rating'] = matches_age_rating[index]
            #new_movie['categories'] = matches_cats[index]
            new_movie['summary'] = re.sub(
                r"<a href=\"https://www.imdb.com/[a-zA-Z_=\?/0-9]*\">",
                r"",
                re.sub(
                    r"</a>",
                    r"",
                    matches_summary[index]
                )
            )
           # new_movie['votes'] = matches_votes[index]
           # new_movie['gross'] = matches_gross[index]
            full_data.append(new_movie)
        # print (len(full_data), file_name)
        # write_file = codecs.open('new_file.html', 'w', 'utf-8')
        # write_file.write(data_second)
        # write_file.close()

    with open('imdb.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'release_year', 'movie_rating',
                      #'meta_score',
                      #'runtime',
                      #'age_rating',
                      #'categories',
                      'summary'
                      #'votes', 'gross'
                      ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in full_data:
            writer.writerow(row)


if __name__ == "__main__":
    main()
