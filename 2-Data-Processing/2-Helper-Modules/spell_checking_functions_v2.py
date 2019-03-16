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
import sys
# Load ENTITY REPLACEMENT
from word_collections import calfresh_placeholders
from text_processing_functions import *

# Designate paths to English and Spanish Corpus Text Files
path_to_english_text0 = os.path.join(os.path.dirname(__file__), '../1-Text-Files/big.txt')
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

def words(text): return re.findall(r'\w+', text.lower())


class Spellchecker():

    def __init__(self, lang="en"):
        """
        Allows Class to load specific languages
        :param lang: language in which to apply spellcheck (string type)
        """
        # load corpuses
        if lang == "en":
            #self.WORDS = Counter(words(open(path_to_english_text).read())) # English Corpus
            self.WORDS = load_eng_counter(path_to_english_text)
        elif lang == "es":
            self.WORDS = Counter(words(open(path_to_spanish_text).read()))
        elif lang == "test":
            self.WORDS = Counter(words(open(path_to_english_text0).read()))
        else:
            print "Only en (English) and es (Spanish) are currently supported"

    def P(self, word):
        """
        Determines probability of `word` based on freq in corpus
        :param word: single word (string type)
        :return: word frequency (float type)
        """
        N = sum(self.WORDS.values())
        return float(self.WORDS[word])/ N

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
        word_list = phrase.split(" ")
        corrections = []
        for word in word_list:
            # only attempt to correct word if it is misspelled
            if check_word(word):
                corrections.append(word)
            else:
                corrections.append(self.correction(word))
        corrected_phrase = " ".join(corrections)
        return corrected_phrase

    def candidates(self, word): 
        """
        Generate possible spelling corrections for word.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, word_list):
        """
        The subset of `words` that appear in the dictionary of WORDS
        :param word_list: list of words
        :return: List of words (list of string types) that are in loaded corpus text
        """
        return set(w for w in word_list if w in self.WORDS)

    def edits1(self, word):
        """
        Generates all edits that are one edit away from `word`.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        """
        Generates all edits that are two edits away from `word`.
        :param word: Single word (string type)
        :return: List of words (list of string types)
        """
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


def spell_correction_language(phrase_tuple):
    phrase = phrase_tuple[0]
    lang = phrase_tuple[1]

    if lang == 'en':
        return en_spellchecker.correction_phrase(phrase)
    elif lang == 'es':
        return es_spellchecker.correction_phrase(phrase)
    elif lang == 'test':
        return test.correction_phrase(phrase)


# Load class instances for each language
# Loading these while loading the module prevents script from having to reload every time
# the spellcheck function is called

# en_spellchecker = Spellchecker("en")
# es_spellchecker = Spellchecker("es")
# test = Spellchecker("test")
#
# print(spell_correction_language(('semester', 'en')))
# print(spell_correction_language(('semester', 'test')))
# print(spell_correction_language(('cuz', 'en')))
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

