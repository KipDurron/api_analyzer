import re

import langdetect
import nltk
from langdetect.lang_detect_exception import ErrorCode

import string
from langdetect import detect
from googletrans import Translator

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

# def translate_to_rus(string):
#     translator = Translator(to_lang="rus")
#     return translator.translate(string)

def translate_rus_to_eng(string):
    translator = Translator()
    return translator.translate(string, src="ru", dest="en").text

# def add_to_rus_dict(string, rus_dict):
#     if string not in rus_dict:
#         elem_rus_dict = {
#             "rus_synonyms": translate_to_rus(string) + []
#         }
#         rus_dict[string] = elem_rus_dict
#
# def add_to_eng_dict(string, eng_dict):
#     if string not in eng_dict:
#         elem_eng_dict = {
#             "synonyms": translate_to_rus(string) + []
#         }
#         eng_dict[string] = elem_eng_dict

def isEnglish(str):
    # try:
    #     return detect(str) == "en"
    # except langdetect.lang_detect_exception.LangDetectException:
    #     return False
    return bool(re.findall(r'[a-z]', str))

def text_with_only_word_and_number(text):
    return re.sub(r'[^a-zа-я0-9 ]', '', text.lower())

def name_api_str_replace(str):
    # убираем название полей json
    str = re.sub(r'"\S+":', '', str)
    # убираем кирилицу
    str = re.sub(r'[а-яёА-ЯЁ]', '', str)
    # убираем единичные буквы типо А
    str = re.sub(r'[\s\W]\w\s', '', str)
    # оставляем только конец пути(например /.../target -> target) и убираем остаток _query или _job
    str = re.sub(r'"\S+/([\w]+)_\w+"(\S+)', r'\1\2', str)
    # оставляем только конец пути(например /.../target -> target)
    # re.sub(r'"\S+/([\w_]+)"(\S+)', r'\1\2', str)
    str = str.replace("'.+':", "").replace("\\n", " ").replace("\n", " ").replace(",", "") \
        .replace(".", "").replace("'", "").replace('"', "").replace(":", "") \
        .replace("[", "").replace("]", "").replace("{", "") \
        .replace("}", "").replace("_", " ").replace("/", " ").replace("(", " ") \
        .replace(")", " ").replace("-", " ").replace("+", " ")
    return str

def normalize_with_wordnet(text):
    text = text_with_only_word_and_number(text)
    """Удаляет знаки пунктуации и заменяет лексемы на нормальные формы с помощью WordNet"""
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    tokens = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]

def get_name_method_by_action(action):
    if action == "to get":
        return "get"
    if action == "to create":
        return "post"
    if action == "to put":
        return "put"
    if action == "to delete":
        return "delete"