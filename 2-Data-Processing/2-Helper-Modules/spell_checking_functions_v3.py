# --------------------------------------------------------------------------------------- ###
#       Functions for Spell Checking and Correction for CFA-Cal-Fresh Project
#       Author: Rocio Ng
#       * Credit to Baolin Liu for an earlier version of code used for a different project
#       Resources:
#           - Frequency Doc for English Words: https://github.com/wolfgarbe/SymSpell
#
# ---------------------------------------------------------------------------------------- ###


# Libraries
import re
from collections import Counter
from langdetect import detect
import os
from nltk.corpus import words, wordnet
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from sacremoses import MosesDetokenizer
from pycontractions import Contractions

detokenizer = MosesDetokenizer()
# Load pre-trained Glove Vector Model - https://nlp.stanford.edu/projects/glove/
# Used for expanding contractions
cont = Contractions(api_key="glove-twitter-25")

# Load ENTITY REPLACEMENT
from word_collections import entity_placeholders
detokenizer = MosesDetokenizer()

# Designate paths to English and Spanish Corpus Text Files
path_to_calfresh_text = os.path.join(os.path.dirname(__file__), '../1-Text-Files/calfresh_text.txt')
path_to_english_text = os.path.join(os.path.dirname(__file__), '../1-Text-Files/frequency_dictionary_en_82_765.txt')
path_to_spanish_text = os.path.join(os.path.dirname(__file__), '../1-Text-Files/spanish-text.txt')

def detect_B(text):
    """
    Customized version of the detect function.
    Adds exception and assigns english to every non-spanish language since most
    applications are english or spanish and detect is not super accurate
    :param text: Single word (string type)
    :return:
    """

    if text is None:
        return "None"
    try:
        lang = detect(text)

        if lang == 'es':
            return lang
        else:
            return 'en'
    except UnicodeDecodeError:
        return "None"


def load_eng_counter(path_to_english_text):
    WORDS = {}
    with open(path_to_english_text, 'r') as text_file:
        for line in text_file:
            word, count = line.strip().split(' ', 1)
            WORDS[word] = int(count)
    return Counter(WORDS)


# ---------------------------------------------------------------------------------- #
# Spell Checker is incorporating logic from:  http://norvig.com/spell-correct.html
# Also See: https://github.com/wolfgarbe/SymSpell, https://github.com/pirate/spellchecker
# --------------------------------------------------------------------------------- #

def word_reader(text): return re.findall(r'\w+', text.lower())


def english_check_corpus():
    nltk_words = set(words.words())
    nltk_wordnet = set(wordnet.words())
    combined_corpus = nltk_words.union(nltk_wordnet)
    return combined_corpus


def expand_contractions(text):
    expanded_text = list(cont.expand_texts([text]))
    return expanded_text[0]


class Spellchecker():
    def __init__(self, lang="en"):
        """
        Allows Class to load specific languages
        :param lang: language in which to apply spellcheck (string type)
        """
        # load corpuses
        if lang == "en":
            self.WORDS = load_eng_counter(path_to_english_text)
            self.CALFRESH_WORDS = Counter(word_reader(open(path_to_calfresh_text).read())) #  Convert CalFresh stories to freq dict
        elif lang == "es":
            self.WORDS = Counter(word_reader(open(path_to_spanish_text).read()))
        else:
            print("Only en (English) and es (Spanish) are currently supported")
        # Load corpuses for checking if words are spelled correctly
        self.english_check_corpus = english_check_corpus()

    @staticmethod
    def check_punctuation(token):
        """
        Checks if token is punctuation
        :param token: tokenized string component
        :return: Boolean
        """
        return token in string.punctuation

    @staticmethod
    def initial_text_processing(text):
        """
        Applies contraction expansion and coerces text to lower case while preserving
        Entity Placeholders
        :param text: String of text, can be a phrase
        :return: Processed String
        """

        # expand contractions
        text = expand_contractions(text)

        # split phrase into tokens
        doc = word_tokenize(text)

        for i in range(len(doc)):
            if doc[i] in entity_placeholders:
                pass
            else:
                doc[i] = doc[i].lower()

        # combine tokens back to string
        processed_phrase = detokenizer.detokenize(doc)
        return processed_phrase

    def check_word(self, word):
        """
        Checks if word is an English Word/Spelled correctly
        :param word: single word (string type)
        :return: Boolean Value
        """
        return word in self.english_check_corpus

    def P(self, word):
        """
        Determines probability of `word` based on freq in corpus
        :param word: single word (string type)
        :return: word frequency (float type)
        """
        N = sum(self.WORDS.values())
        return float(self.WORDS[word]) / N

    def correction(self, word):
        """
        Determines the most probable spelling correction for a word
        :param word: single word (string type)
        :return: word with highest probability (string type)
        """
        return max(self.candidates(word), key=self.P)

    def correction_phrase(self, phrase):
        """
        Correction function applied to each word in phrase
        :param phrase: Phrase of multiple words (string type)
        :return: Phrase with Spell Correction Applied (string type)
        """

        # split phrase into tokens
        doc = word_tokenize(phrase)

        for i in range(len(doc)):
            # checks if punctuation
            if self.check_punctuation(doc[i]):
                pass
            # only attempt to correct word if it is misspelled
            elif self.check_word(doc[i]) or doc[i] in entity_placeholders:
                pass
            else:
                doc[i] = self.correction(doc[i])

        # combine tokens back to string
        corrected_phrase = detokenizer.detokenize(doc)

        return corrected_phrase

    def candidates(self, w):
        """
        Generate possible spelling corrections for word prioritizing CalFresh known words over corpus.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        result =  (self.known_calfresh([w]) 
            or self.known_calfresh(self.edits1(w)) 
            or self.known_calfresh(self.edits2(w)) 
            or self.known([w]) 
            or self.known(self.edits1(w)) 
            or self.known(self.edits2(w)) 
            or [w])

        return result

    def known(self, word_list):
        """
        The subset of `words` that appear in the dictionary of WORDS
        :param word_list: list of words
        :return: List of words (list of string types) that are in loaded corpus text
        """
        return set(w for w in word_list if w in self.WORDS)

    def known_calfresh(self, word_list):
        """
        The subset of `words` that appear in the dictionary of CALFRESH_WORDS
        :param word_list: list of words
        :return: List of words (list of string types) that are in loaded calfresh corpus text
        """
        return set(w for w in word_list if w in self.CALFRESH_WORDS)

    def edits1(self, word):
        """
        Generates all edits that are one edit away from `word`.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """
        Generates all edits that are two edits away from `word`.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


# Load class instances for each language
# Loading these while loading the module prevents script from having to reload every time
# the spellcheck function is called

en_spellchecker = Spellchecker("en")
es_spellchecker = Spellchecker("es")


def spell_correction_language(phrase_tuple):
    phrase = phrase_tuple[0]
    lang = phrase_tuple[1]

    if lang == 'en':
        return en_spellchecker.correction_phrase(phrase)
    elif lang == 'es':
        return es_spellchecker.correction_phrase(phrase)


# test = Spellchecker("test")
#
#print(spell_correction_language(('semestre', 'en')))
#print(spell_correction_language(('semestre', 'es')))
# print(spell_correction_language(('semester', 'test')))
# print(spell_correction_language(('PERSON', 'en')))
# print(spell_correction_language(('cuz', 'test')))
# print(spell_correction_language(('penut', 'en')))
# print(spell_correction_language(('penut', 'test')))
# print(spell_correction_language(('kids', 'en')))
# print(spell_correction_language(('kids', 'test')))
# print(spell_correction_language(('developmentally', 'en')))
# print(spell_correction_language(('developmentally', 'test')))
# print(spell_correction_language(('daddi and moms', 'en')))
# print(spell_correction_language(('daddi and moms', 'test')))
# print(spell_correction_language(('hiv', 'en')))
# print(spell_correction_language(('hiv', 'test')))
# print(en_spellchecker.WORDS)
#print(spell_correction_language(('the cat, is   undar the tree  .', 'en')))
#print (en_spellchecker.initial_text_processing("she's coming top the test PERSON, PLACE thing"))
#print (en_spellchecker.initial_text_processing("I;m comign home, I'm coming im coming"))
#print (en_spellchecker.expand_contractions("she's shes coming"))