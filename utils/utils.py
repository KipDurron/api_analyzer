import re
from translate import Translator

def get_words_dict(words):
    temp_dict = {}
    for word in words:
        if word in temp_dict:
            temp_dict[word] = temp_dict[word] + 1
        else:
            temp_dict[word] = 1
    return temp_dict

def replace_char(string, prev_char, new_char):
   return string.replace(prev_char, new_char)

def translate_to_rus(string):
    translator = Translator(to_lang="rus")
    return translator.translate(string)

def add_to_rus_dict(string, rus_dict):
    if string not in rus_dict:
        elem_rus_dict = {
            "rus_synonyms": translate_to_rus(string) + []
        }
        rus_dict[string] = elem_rus_dict

def add_to_eng_dict(string, eng_dict):
    if string not in eng_dict:
        elem_eng_dict = {
            "synonyms": translate_to_rus(string) + []
        }
        eng_dict[string] = elem_eng_dict
