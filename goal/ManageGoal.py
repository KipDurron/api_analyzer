import pymorphy2
import nltk
from goal.ActionGoal import ActionGoal
from translate import Translator
import re

from utils.utils import isEnglish

ACTION_NOT_FOUND = "action не определён"

def get_goal_from_request(user_request = "я хочу создать наверное instance с cpu = 10"):
    morph = pymorphy2.MorphAnalyzer()
    request_without_bad_char = re.sub(r'[^a-zа-я0-9 ]', '', user_request.lower())
    request_arr = re.sub(r'\s+', ' ', request_without_bad_char).split(" ")
    result_get_action = get_action(request_arr, morph)
    if result_get_action != ACTION_NOT_FOUND:
        object_goal = get_object(request_arr, result_get_action, morph)
        goal = {"action_goal": result_get_action["action_goal"], "object_goal": object_goal}
        return goal
    else:
        return ACTION_NOT_FOUND


def get_object(request_arr, result_get_action, morph):
    # tokens = nltk.pos_tag(request_arr)
    index_distance_arr = []
    i = 0
    while i < len(request_arr):
        # if isEnglish(request_arr[i]):
        #     check_word = Translator(to_lang="rus").translate(request_arr[i])
        # else:
        #     check_word = request_arr[i]
        check_word = request_arr[i]
        # если слово английское и находится оно существительное NN и сущ во множ числе NNS, то это нам подходит
        if isEnglish(check_word):
            if (nltk.pos_tag([check_word])[0][1] == "NN" or nltk.pos_tag([check_word])[0][1] == "NNS") and i != result_get_action["action_index"]:
                index_distance_arr.append({"index": i, "distance": abs(i - result_get_action["action_index"])})
        i += 1
    min_index_distance = min(index_distance_arr, key=lambda item: item["distance"])["index"]
    object_goal = request_arr[min_index_distance]
    return object_goal

def get_action(request_arr, morph):
    for word in request_arr:
        p = morph.parse(word)[0]
        if p.tag.POS == "INFN" or p.tag.POS == "VERB":
            action_index = request_arr.index(word)
            norm_form_action = p.normalized.normal_form
            actions = ActionGoal().actions
            for key, value in actions.items():
                if value == norm_form_action:
                    action_goal = key
                    return {"action_goal" : action_goal, "action_index" : action_index}
    return ACTION_NOT_FOUND

get_goal_from_request()