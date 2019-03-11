"""
Features to consider for each n-gram (ZERO / ONE)

1) Capitalization - if first letter(s) capitalized unless de / von / van
2) 'al-<capital>...'
3) Mr / Dr / Mrs / Ms / Deputy / Chief / President
   Senator / Sen. etc                                  before
4) administration / regime etc                         after
5) said / asked / told                                 before OR after
6) <comma> <number> <comma>                            after
7) <paranthesis>                                       before AND after
8) hyphenated ?
9) the / a / an                                        before
10) in / at / on                                       before
11) @...
12) comma in middle of phrase
13) possessive ('s) in word
14) number of words
15) if a period or question marks exists before during or after
16) jr / sr / iii / iv / v in word
17) common word in current
18) if len is > 2
19) check if at least one lower case
20) check if previous word has first capital and no possessive

BLACKLIST : Deputy / Chief / President / Senator / Sen. / CNN
"""

capital_blacklist = ["de", "von", "van", "bin"]


def capital_check(words):
    #caps = 0
    #for word in words[1]:
    #    caps += 1 if (len(word) > 0 and (word[0].isupper() or any(y == word for y in capital_blacklist))) else 0
    return any(len(x) > 0 and (x[0].isupper() or any(y == x for y in capital_blacklist)) for x in words[1])


def al_check(words):
    return any((len(x) > 3 and x[:3] == 'al-' and x[3].isupper()) for x in words[1])


prefix_whitelist = [
    "mr", "dr", "mrs", "ms", "miss", "deputy", "chief", "president", "spokesman",
    "spokeswoman", "senator", "sen", "republican", "rep", "democratic", "dem",
    "secretary", "minister", "sir", "lord", "ambassador", "rev", "col", "lt", "adm",
    "commissioner"
]


def prefix_check(words):
    return any((x.replace(".", "").lower() in prefix_whitelist for x in words[0]))


suffix_whitelist = [
    "administration"
]


def suffix_check(words):
    return any((x.replace(".", "").lower() in suffix_whitelist for x in words[2]))


verb_whitelist = [
    "said", "told", "asked", "called"
]


def verb_check(words):
    return any((x.replace(".", "").lower() in verb_whitelist for x in (words[0] + words[2])))


def comma_number_after_check(words):
    try:
        return True if len(words[2]) > 2 and words[2][0] == "," and words[2][2] == "," and \
                       int(words[2][1]) < 130 else False
    except ValueError:
        return False


def parenthetical_check(words):
    return True if len(words[0]) > 0 and len(words[2]) > 0 and \
                   words[0][-1] == '(' and words[2][0] == ')' else False


def hyphenated_check(words):
    return any("-" in x for x in words[1])


prefix_article_whitelist = [
    "the", "a", "an"
]


def prefix_article_check(words):
    return not any((x.replace(".", "").lower() in prefix_article_whitelist for x in words[0]))



prefix_preposition_whitelist = [
    "in", "on", "at"
]


def prefix_preposition_check(words):
    return not any((x.replace(".", "").lower() in prefix_preposition_whitelist for x in words[0]))


def atter_checker(words):
    return not any((len(x) > 0 and x[0] == '@') for x in words[1])


def comma_middle_check(words):
    return not any("," in x for x in words[1])


def possessive_check(words):
    return True if len(words[1]) > 0 and words[1][-1].endswith("\'s") else False


def num_words(words):
    return len(words[1])


def check_punctuation(words):
    val = False
    for lis in words:
        val = val or any("." in x for x in lis) or any("?" in x for x in lis) or \
              any("?" in x for x in lis)
    return not val


prefix_jr_sr_whitelist = [
    "jr", "sr"
]


def jr_sr_check(words):
    return any((x.replace(".", "").lower() in prefix_jr_sr_whitelist for x in words[1]))


common_words = [
    'if', 'of', 'it', 'he', 'it\'s', 'who', 'we', 'the', 'new',
    'i', 'a', 'she', 'was', 'why', 'what', 'they', 'but', 'for',
    'your'
]

def common_word_checker(words):
    return not any((x.replace(".", "").lower() in common_words for x in words[1]))


def len_word(words):
    return not any(len(x.replace(".", "")) <= 2 for x in words[1])


def last_capital(words):
    return True if len(words[0]) > 0 and len(words[0][-1]) > 0 and \
                   words[0][-1][0].isupper() and not words[0][-1][0].endswith("\'s") else False


_VECTORIZER_NAMES_ = [
    'capital_check',
    'al_check',
    'prefix_check',
    'suffix_check',
    'verb_check',
 #   'comma_number_after_check',
    #'parenthetical_check',
 #   'hyphenated_check',
    'prefix_article_check',
    'prefix_preposition_check',
   # 'atter_checker',
   # 'comma_middle_check',
    'possessive_check',
    'num_words',
    #'check_punctuation',
    'jr_sr_check',
    'common_word_checker',
    #'last_capital'
]


_VECTORIZER_ = [
    capital_check,
    al_check,
    prefix_check,
    suffix_check,
    verb_check,
#    comma_number_after_check,
#    parenthetical_check,
#    hyphenated_check,
    prefix_article_check,
    prefix_preposition_check,
 #   atter_checker,
#    comma_middle_check,
    possessive_check,
    num_words,
 #   check_punctuation,
    jr_sr_check,
   common_word_checker,
   # last_capital
]


_BLACKLIST_PART_ = [
    "cnn", "mashable",  "japan", "cnn\'s", "australia", "japan",
    "state", "al-qaeda", "al-adha", "just", "before", "first",
    "more", "us", "@highlight", "new:", "hw"
] + prefix_whitelist + suffix_whitelist + verb_whitelist + common_words

_BLACKLIST_ = ["jr", "sr"]

"""
:param xwords - any words previous to current
:param ywords - any words currently being considered
:param zwords - any following words
"""
def vectorize_phrase(xwords, ywords, zwords, vectorizers=_VECTORIZER_):
    return [vectorizer([
        [x.replace("\"", "") for x in xwords],
        [x.replace("\"", "") for x in ywords],
        [x.replace("\"", "") for x in zwords]
    ]) for vectorizer in vectorizers]


def in_blacklist(words):
    return any(x.replace("\"", "").replace(".", "").lower() in _BLACKLIST_PART_ for x in words) or \
           (len(words) == 1 and len(words[0]) > 0 and words[0] in _BLACKLIST_)
