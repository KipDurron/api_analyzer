from classifiers.ClassifierObjects import ClassifierObjects
from goal.TakeGoal import get_goal_from_request
from proximity_measure.ProximityMeasure import ProximityMeasure
from statistics.statistic_api_conf import StatisticApiConf
from api_request.api_analyzer_request import ApiAnalyzerRequest
import nltk

def start_app():
    api_analyzer_request = ApiAnalyzerRequest('http://sbcloud.ru/api/swagger')
    stat_api_config = StatisticApiConf(api_analyzer_request)
    classifierObjects = ClassifierObjects(api_analyzer_request.json_response)
    user_request = "я хочу обновить наверное instance с cpu = \"10\""
    pm = ProximityMeasure(user_request, get_goal_from_request(user_request), stat_api_config, classifierObjects)
    pm.PM_goal_with_api_functions()
    pm.PM_user_request_with_api_functions()
    print(stat_api_config.word_stat)


start_app()