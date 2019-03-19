### ---------------------------------------------------------------------------------- ###
#       Text Processing Functions for Cal-Fresh Project 
#
### ---------------------------------------------------------------------------------- ###
from word_collections import calfresh_placeholders # These are entity replacement keywords that should stay capitalized
import enchant
from enchant.checker import SpellChecker
from word_collections import entity_placeholders

def removePunctuation(text):
    '''
    Removes Punctuation from Input Text
    :param text: Text Input
    :return: Text free of punctuation
    '''

    for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
        text = text.replace(c,"")
    return text


def initial_phrase_processing(text):
    try:
        split_text = text.split(" ")
        # only process words that are not a entity calfresh placeholder
        processed_text_list = [word.lower().strip() if word not in entity_placeholders else word for word in split_text]
        processed_text_list = [removePunctuation(word) for word in processed_text_list if word !=""]
        processed_text = " ".join(processed_text_list)
        return processed_text
    
    except AttributeError:
        return None