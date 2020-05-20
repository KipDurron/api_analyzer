import pymorphy2
import nltk

from goal.ActionGoal import ActionGoal

ACTION_NOT_FOUND = "action не определён"

def get_goal_from_request(user_request = "создать instance с cpu = 10"):
    request_arr = user_request.split(" ")
    result_get_action = get_action(request_arr)
    if result_get_action != ACTION_NOT_FOUND:
        request_arr[result_get_action["action_index"]] = result_get_action["action_goal"]
        object_goal = get_object(request_arr, result_get_action)
        goal = {"action_goal": result_get_action["action_goal"], "object_goal": object_goal}
        return goal
    else:
        return ACTION_NOT_FOUND


def get_object(request_arr, result_get_action):
    tokens = nltk.pos_tag(request_arr)
    i = 0
    index_distance_arr = []
    i = 0
    while i < len(tokens):
        if tokens[i][1] == "NN" and i != result_get_action["action_index"]:
            index_distance_arr.append(abs(i - result_get_action["action_index"]))
        i += 1
    min_index_distance = min(index_distance_arr)
    object_goal = tokens[min_index_distance][0]
    return object_goal

def get_action(request_arr):
    morph = pymorphy2.MorphAnalyzer()
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