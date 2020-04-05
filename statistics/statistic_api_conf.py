import json
import re
import collections
from utils import utils

class StatisticApiConf:

    def __init__(self, request):
        self.word_stat = {}
        self.common_world_stat = {}
        self.count_words_in_api_func(request)


    def count_words_in_api_func(self, request):
        string_oper = ''
        common_string_oper = ''
        for path, operations in request.json_response.get('paths').items():
            # print(path, operations)
            string_oper += json.dumps(operations, ensure_ascii=False) + ' ' + path
            # убираем название полей json
            string_oper = re.sub(r'"\S+":', '', string_oper)
            # убираем кирилицу
            string_oper = re.sub(r'[а-яёА-ЯЁ]', '', string_oper)
            # убираем единичные буквы типо А
            string_oper = re.sub(r'[\s\W]\w\s', '', string_oper)
            # оставляем только конец пути(например /.../target -> target) и убираем остаток _query или _job
            string_oper = re.sub(r'"\S+/([\w]+)_\w+"(\S+)', r'\1\2', string_oper)
            # оставляем только конец пути(например /.../target -> target)
            # re.sub(r'"\S+/([\w_]+)"(\S+)', r'\1\2', string_oper)
            string_oper = string_oper.replace("'.+':", "").replace("\\n", " ").replace("\n", " ").replace(",", "")\
                .replace(".", "").replace("'", "").replace('"', "").replace(":", "")\
                .replace("[", "").replace("]", "").replace("{", "")\
                .replace("}", "").replace("_", " ").replace("/", " ").replace("(", " ")\
                .replace(")", " ").replace("-", " ").replace("+", " ")
            words = string_oper.split()
            self.word_stat[path] = utils.get_words_dict(words)
            common_string_oper += string_oper
        words = common_string_oper.split()
        self.common_world_stat = utils.get_words_dict(words)
        self.common_world_stat = collections.OrderedDict(sorted(self.common_world_stat.items()))

    # def get_words_dict(self, words):
    #     temp_dict = {}
    #     for word in words:
    #         if word in temp_dict:
    #             temp_dict[word] = temp_dict[word] + 1
    #         else:
    #             temp_dict[word] = 1
    #     return temp_dict





