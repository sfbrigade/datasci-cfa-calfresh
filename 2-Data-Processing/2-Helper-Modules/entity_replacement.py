#import packages
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.vocab import Vocab
import re


#declarations

nlp = spacy.load('en')
nlp_multilingual = spacy.load('en_core_web_sm')
tracked_entities = ['PERSON','ORG','GPE','LOC','DATE','MONEY','CARDINAL']
names = "Abhishek, edwig, EDUARDO and mary are going for a run"
test = "Abhishek, edwig, EDUARDO and mary are going for a run"

def is_name(text):
    return text in names


#helper functions

#define vocab list of entities and flag token fititng criteria with NAME
def name_placeholder(text):
    NAME = nlp.vocab.add_flag(is_name)
    NAME = nlp_multilingual.vocab.add_flag(is_name)
    doc_m = nlp_multilingual(text)
    whitelist_text = text
    for token in doc_m:
        if token.check_flag(NAME):
            whitelist_text = whitelist_text.replace(token.text, "NAME")
    return whitelist_text


#implement entity replacement by removing listed entities using flagged tokens 
def recognizer(text):
    try:
        doc = nlp(text)
        anon_comment = text
        for ent in doc.ents:
            if ent.text not in STOP_WORDS and ent.label_ in tracked_entities:
                anon_comment = anon_comment.replace(ent.text, ent.label_)
        return name_placeholder(anon_comment)
    except:
        print(text)
        pass


#locate punctuation and apply whitespace as padding around target
def paddingFunc(text):
    text = re.sub('([.,!?()])', r' \1 ', text)
    text = re.sub('\s{2,}', ' ', text)
    return text



#original entity replacement code for reference
'''# -*- coding: utf-8 -*-
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.vocab import Vocab
import pandas as pd
import numpy as np
import os
import xx_ent_wiki_sm

nlp = spacy.load('en_core_web_sm')

#python -m spacy download xx for multilingual processing
nlp_multilingual = xx_ent_wiki_sm.load()

from spacy.lang.en.stop_words import STOP_WORDS
STOP_WORDS.add("calfresh")
STOP_WORDS.add("CalFresh")
STOP_WORDS.add("Calfresh")
STOP_WORDS.add("Cal")
STOP_WORDS.add("cal")
STOP_WORDS.add("fresh")
STOP_WORDS.add("Fresh")
STOP_WORDS.add("food")f
STOP_WORDS.add("Food")
STOP_WORDS.add("stamps")
STOP_WORDS.add("Stamps")
STOP_WORDS.add("SAR7")
STOP_WORDS.add("SAR")
STOP_WORDS.add("sar")
STOP_WORDS.add("sar7")
STOP_WORDS.add("SR7")
STOP_WORDS.add("SAR-7")
STOP_WORDS.add("Sar-7")
STOP_WORDS.add("sar-7")
STOP_WORDS.add("SR7")
STOP_WORDS.add("sr7")
STOP_WORDS.add("ebt")
STOP_WORDS.add("EBT")
STOP_WORDS.add("NAME")

tracked_entities = ['PERSON','ORG','GPE','LOC','DATE','MONEY','CARDINAL']
#reading in the CSV file
#infile=pd.read_csv("additional_comments.csv")
#infile=infile[0:100]

# reading in the file of names (8500 names) into a list to flag
my_project_dir = os.path.dirname('__file__')
names_file = os.path.join(my_project_dir, 'data', 'firstnames.csv')
test_file = os.path.join(my_project_dir, 'data', 'testnames.txt')
names = []

with open(names_file, 'r') as fp:
    for line in fp.readlines():
        name = str(line.strip())
        names.append(name.lower())
        names.append(name.title())

def is_name(text):
    return text in names

# constructing a vocab list for names
# Integration list of first names and spacy vocab
# 1. load a list from disk
# 2. transform: upper(), lower(), title()
# 3. save as vocab list with a flag
# 4. flag if token is in the list of names (placeholder)
# 5. test on made-up dataset (created using Faker) after running spacy's NER
# 6. test on a subset of a real dataset

NAME = nlp.vocab.add_flag(is_name)
NAME = nlp_multilingual.vocab.add_flag(is_name)

def name_placeholder(text):
    doc_m = nlp_multilingual(text)
    whitelist_text = text
    for token in doc_m:
        if token.check_flag(NAME):
            whitelist_text = whitelist_text.replace(token.text, "NAME")
    return whitelist_text

test = "Abhishek, edwig, EDUARDO and mary are going for a run"
print(name_placeholder(test))

#https://spacy.io/api/token
def recognizer (original_comment):
    try:
        doc = nlp(original_comment)
        anon_comment = original_comment
        for ent in doc.ents:
            if ent.text not in STOP_WORDS and ent.label_ in tracked_entities:
                anon_comment = anon_comment.replace(ent.text, ent.label_)
        return name_placeholder(anon_comment)
    except:
        print(original_comment)
        pass

#infile['entity_replacement'] = infile['additional_information'].apply(lambda comment: recognizer(comment))
#infile.to_csv('additional_comments_entity_replacement_with_names.csv')
'''
