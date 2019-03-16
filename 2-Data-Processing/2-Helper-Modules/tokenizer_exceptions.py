# Install pyenchant: PyEnchant https://github.com/rfk/pyenchant
# Install spaCy: pip install spacy && python -m spacy download en
from __future__ import unicode_literals, print_function
import spacy
from spacy.attrs import ORTH, LEMMA, NORM, TAG
from spacy.tokenizer_exceptions import TOKENIZER_EXCEPTIONS
# from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
# from spacy.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.util import update_exc
import enchant
import json
import re

nlp = spacy.load('en_core_web_sm')
doc = nlp(
    "This sentence ain't gonna be ORG grammatically correct7. 9 >>{:o) THis sentence about SAR7 PERSON doesn't have mispeled wordz.")
d = enchant.Dict('en_US')

# dealing with contractions
TOKENIZER_EXCEPTIONS = {
    # do
    "don't": [
        {ORTH: "do", LEMMA: "do"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "doesn't": [
        {ORTH: "does", LEMMA: "do"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "didn't": [
        {ORTH: "did", LEMMA: "do"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    # can
    "can't": [
        {ORTH: "ca", LEMMA: "can"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "couldn't": [
        {ORTH: "could", LEMMA: "can"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    # have
    "I've'": [
        {ORTH: "I", LEMMA: "I"},
        {ORTH: "'ve'", LEMMA: "have", NORM: "have", TAG: "VERB"}],
    "haven't": [
        {ORTH: "have", LEMMA: "have"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "hasn't": [
        {ORTH: "has", LEMMA: "have"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "hadn't": [
        {ORTH: "had", LEMMA: "have"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    # will/shall will be replaced by will
    "I'll'": [
        {ORTH: "I", LEMMA: "I"},
        {ORTH: "'ll'", LEMMA: "will", NORM: "will", TAG: "VERB"}],
    "he'll'": [
        {ORTH: "he", LEMMA: "he"},
        {ORTH: "'ll'", LEMMA: "will", NORM: "will", TAG: "VERB"}],
    "she'll'": [
        {ORTH: "she", LEMMA: "she"},
        {ORTH: "'ll'", LEMMA: "will", NORM: "will", TAG: "VERB"}],
    "it'll'": [
        {ORTH: "it", LEMMA: "it"},
        {ORTH: "'ll'", LEMMA: "will", NORM: "will", TAG: "VERB"}],
    "won't": [
        {ORTH: "wo", NORM: "would", LEMMA: "will"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "wouldn't": [
        {ORTH: "would", LEMMA: "will"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    # be
    "I'm'": [
        {ORTH: "I", LEMMA: "I"},
        {ORTH: "'m'", LEMMA: "be", NORM: "am", TAG: "VERB"}],
    "wasn't": [
        {ORTH: "was", LEMMA: "be"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}],
    "isn't": [
        {ORTH: "is", LEMMA: "be"},
        {ORTH: "n't", LEMMA: "not", NORM: "not", TAG: "RB"}]
}
TOKENIZER_EXCEPTIONS = update_exc(TOKENIZER_EXCEPTIONS)

# updating the stopset
calfresh_stopwords = {"Calfresh", "CalFresh", "calfresh", "CALFRESH", "foodstamps", "sar7", "sar", "sr7", "sr", "SAR7",
                      "SR7", "SAR", "SR", "Sar", "Sar7", "ebt"}
calfresh_placeholders = {"PERSON", "ORG", "GPE", "LOC", "DATE", "MONEY", "CARDINAL"}
stopset = STOP_WORDS.update(calfresh_stopwords, calfresh_placeholders)

regex = re.compile(r'\W|\d', flags=re.UNICODE)


def clean_words(text):
    try:
        text = regex.sub('', text)
    except:
        pass
    return text


def enchant_spellchecker(doc):
    for token in doc:
        word = token.text
        # print(token.text, token.lemma_, token.is_punct, token.is_digit, token.is_alpha)
        if token.is_stop or token.is_punct:
            print(word)
        elif token.is_alpha:  # is \w
            if d.check(word):
                print(word)
            else:
                corrections = d.suggest(word)
                if len(corrections) > 0:
                    print("Misspelled word: {}".format(word))
                    print("Suggested corrections: {}".format(corrections[0]))
                else:
                    print("ERROR_PLACEHOLDER")
        elif token.is_digit:  # is \d
            print("NUMBER_PLACEHOLDER")
        else:
            try:
                word_clean = clean_words(word)
                if len(word_clean) > 0:
                    corrections = d.suggest(clean_words(token.text))
                    print("Misspelled word: {}".format(token.text))
                    print("Suggested corrections: {}".format(corrections[0]))
            except:
                print("ERROR_PLACEHOLDER")

enchant_spellchecker(nlp("mom wasn't home she'll don't calfresh"))
