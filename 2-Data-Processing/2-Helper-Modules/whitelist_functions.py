# ---------------------------------------------------------------------------------- ###
#       Functions for Whitelisting Documents for CFA-Cal-Fresh Project
#       Author: Rocio Ng
# ---------------------------------------------------------------------------------- ###

import os
import pandas as pd
from text_processing_functions import *

path_to_wl1 = os.path.join(os.path.dirname(__file__), '../1-Text-Files/1-White-List-Docs/white-list.csv')
path_to_wl2 = os.path.join(os.path.dirname(__file__), '../1-Text-Files/1-White-List-Docs/wordsEn.csv')


# Load text documents
whitelist_df1 = pd.read_csv(path_to_wl1)
whitelist_df2 = pd.read_csv(path_to_wl2)
whitelist_list1 = whitelist_df1["word"].tolist()
whitelist_list2 = whitelist_df2["word"].tolist()


def text_to_csv(path_to_txt, path_to_csv):
    in_txt = csv.reader(open(path_to_txt, "rb"), delimiter = '\t')
    out_csv = csv.writer(open(path_to_csv, 'wb'))
    out_csv.writerows(in_txt)


whitelist_list = whitelist_list1 + whitelist_list2


def check_whitelist(phrase, whitelist, method):
    # clean phrase and split into words
    phrase = phrase.lower().strip()
    phrase = removePunctuation(phrase)
    word_list = phrase.split(" ")

    # word_list = re.findall(r"[\w']+|[.,!?;]", phrase)
    word_list = [word for word in word_list if word != ""]  # for clearing double spaces

    # remove words not in white list and calculate # of words removed
    if method == "remove":
        cleaned_word_list = [word for word in word_list if word in whitelist]
        delta = len(word_list) - len(cleaned_word_list)
        cleaned_phrase = " ".join(cleaned_word_list)
    elif method == "replace":
        cleaned_word_list = [word if word in whitelist else "[redacted]" for word in word_list]
        cleaned_phrase = " ".join(cleaned_word_list)
        delta = cleaned_word_list.count("[redacted]")
    return cleaned_phrase, delta


def removed_words(phrase, whitelist):
    pass


#test_phrase = "This is a Test.   For Rocio. Hello. "
#print(check_whitelist(test_phrase, whitelist_list, "replace"))