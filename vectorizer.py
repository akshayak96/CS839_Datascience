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
10) in / at / on                                        before
11) @...

BLACKLIST : Deputy / Chief / President / Senator / Sen. / CNN
"""


def capital_check(words):
    capital_blacklist = ["de", "von", "van"]
    return all(((len(x) > 0 and x[0].isupper()) or any(y == x for y in capital_blacklist)) for x in words[1])


def al_check(words):
    return any((len(x) > 3 and x[:3] == 'al-' and x[3].isupper()) for x in words[1])


def prefix_check(words):
    prefix_whitelist = [
        "mr", "dr", "mrs", "ms", "deputy", "chief", "president", "spokesman",
        "spokeswoman", "senator", "sen", "republican", "rep", "democratic", "dem"
    ]
    return any((x.replace(".", "").lower() in prefix_whitelist for x in words[0]))


def suffix_check(words):
    suffix_whitelist = [
        "administration", "regime", "spokesman", "spokeswoman"
    ]
    return any((x.replace(".", "").lower() in suffix_whitelist for x in words[2]))


def verb_check(words):
    verb_whitelist = [
        "said", "told", "asked"
    ]
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


def prefix_article_check(words):
    prefix_article_whitelist = [
        "the", "a", "an"
    ]
    return any((x.replace(".", "").lower() in prefix_article_whitelist for x in words[0]))


def prefix_preposition_check(words):
    prefix_preposition_whitelist = [
        "in", "on", "at"
    ]
    return any((x.replace(".", "").lower() in prefix_preposition_whitelist for x in words[0]))


def atter_checker(words):
    return any((len(x) > 0 and x[0] == '@') for x in words[1])


_VECTORIZER_ = [
    capital_check,
    al_check,
    prefix_check,
    suffix_check,
    verb_check,
    comma_number_after_check,
    parenthetical_check,
    hyphenated_check,
    prefix_article_check,
    prefix_preposition_check,
    atter_checker
]


_BLACKLIST_ = [
    "Deputy", "Chief", "President", "Senator", "Sen.",  "CNN", "Mashable"
]

"""
:param xwords - any words previous to current
:param ywords - any words currently being considered
:param zwords - any following words
"""
def vectorize_phrase(xwords, ywords, zwords, vectorizers=_VECTORIZER_):
    return [vectorizer([xwords, ywords, zwords]) for vectorizer in vectorizers]


def in_blacklist(yword):
    return yword in _BLACKLIST_
