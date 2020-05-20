from classifiers.ClassifierObjects import ClassifierObjects
from statistics.statistic_api_conf import StatisticApiConf
from api_request.api_analyzer_request import ApiAnalyzerRequest
import nltk

def start_app():





    api_analyzer_request = ApiAnalyzerRequest('http://sbcloud.ru/api/swagger')
    stat_api_config = StatisticApiConf(api_analyzer_request)
    classifierObjects = ClassifierObjects(api_analyzer_request.json_response)
    print(stat_api_config.word_stat)


start_app()