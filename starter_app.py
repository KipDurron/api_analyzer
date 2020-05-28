from classifiers.ClassifierObjects import ClassifierObjects
from goal.TakeGoal import get_goal_from_request, ACTION_NOT_FOUND
from proximity_measure.ProximityMeasure import ProximityMeasure
from statistics.statistic_api_conf import StatisticApiConf
from api_request.api_analyzer_request import ApiAnalyzerRequest
import nltk

def start_app():
    api_analyzer_request = ApiAnalyzerRequest('http://sbcloud.ru/api/swagger')
    stat_api_config = StatisticApiConf(api_analyzer_request)
    classifierObjects = ClassifierObjects(api_analyzer_request.json_response)
    user_request = "я хочу создать наверное instance с software = \"Microsoft\""
    goal = get_goal_from_request(user_request)
    if goal == ACTION_NOT_FOUND:
        print(ACTION_NOT_FOUND)
    else:
        pm = ProximityMeasure(user_request, goal, stat_api_config, classifierObjects)
        result_program = pm.PM_goal_with_api_functions(pm.goal, pm.get_req_params(user_request))
        pm.print_result(result_program)


start_app()