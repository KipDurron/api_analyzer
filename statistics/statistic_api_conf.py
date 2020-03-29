import requests
from urllib.request import urlopen
import json
import certifi


class statistic_api_conf:

    def __init__(self, url_api_conf):
        self.url_api_conf = url_api_conf
        self.response = requests.get(self.url_api_conf, verify=False)
        self.json_response = self.response.json()
        self.word_stat = {}
        self.count_words_in_api_func()


    def count_words_in_api_func(self):
        for key, value in self.json_response.get('paths').items():
            print(key, " - ", value)





