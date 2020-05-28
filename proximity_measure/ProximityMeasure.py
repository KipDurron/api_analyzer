import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transliterate.conf import settings
import re
import json

from utils.utils import normalize_with_wordnet, name_api_str_replace, translate_rus_to_eng, get_name_method_by_action

NOT_FOUND_API_CONST = "Поиск функция api по вашему запросу не дал результата"

class ProximityMeasure:
    def __init__(self, user_request, goal, stat_api_config, classifierObjects):
        self.req_params_dict = self.get_req_params(user_request)
        self.user_request = translate_rus_to_eng(user_request)
        # self.goal_sentence = goal["action_goal"] + " " + goal["object_goal"]["value"]
        self.goal = goal
        # self.goal_sentence = "hello world"
        self.arr_api_names = [key for key in stat_api_config.word_stat.keys()]
        # self.arr_api_sentences = self.get_arr_api_sentences(stat_api_config)
        self.arr_api_sentences = self.get_arr_api_sentences_from_api_names(self.arr_api_names)
        self.classifierObjects = classifierObjects.classifierObjects

    def get_req_params(self, user_request):
        return dict(re.findall(r'(\S+)\s+=\s+"(.*?)"', user_request))

    def get_arr_api_sentences_from_api_names(self, arr_api_names):
        return_arr_sentences = []
        for sentence in arr_api_names:
            return_arr_sentences.append(name_api_str_replace(sentence))
        return return_arr_sentences

    def get_arr_api_sentences(self, stat_api_config):
        return_arr_sentences = []
        for func_api_stat in stat_api_config.word_stat.values():
            sentence = ""
            for word, count in func_api_stat.items():
                for i in range(1, count + 1):
                    sentence += word + " "
            return_arr_sentences.append(sentence)
        return return_arr_sentences

    # def PM_user_request_with_api_functions(self):
    #     out = self.find_api_by_tfidf(self.user_request)
    #     return out

    def print_result(self, item_res_api):
        # print_item =  json.dumps(item_res_api)
        print(json.dumps(item_res_api, indent=4, sort_keys=True, ensure_ascii=False))


    def set_req_body(self, request_body_str, param_for_req_body):
        if not bool(param_for_req_body):
            return {}
        request_body_json = json.loads(request_body_str)
        return_request_body = {}
        for param_name, param_value in param_for_req_body.items():
            # request_body_str = re.sub("(\'" + param_name + "\': )\'[\w_]+\'", r'\1' + param_value, request_body_str)
            if "properties" in request_body_json:
                properties = request_body_json["properties"]
                if param_name in properties:
                    return_request_body[param_name] = param_value

        return return_request_body



    def PM_goal_with_api_functions(self, goal, param_for_req_body, pred_api_name = ""):
        api_name = self.find_api_by_tfidf(goal["object_goal"]["value"], goal)
        if api_name == NOT_FOUND_API_CONST or pred_api_name == api_name:
            return {"api_name": NOT_FOUND_API_CONST,
                    "goal": goal}
        method = get_name_method_by_action(goal["action_goal"])
        req_body = {}
        used_api = []
        if api_name in self.classifierObjects:
            classifierObject = self.classifierObjects[api_name]
            params_path = classifierObject.params_path
            if method in classifierObject.actions:
                action_content = classifierObject.actions[method]
                used_params = action_content['used_params']
                request_body_str = action_content['request_body_str']
                req_body = self.set_req_body(request_body_str, param_for_req_body)
                for used_param in used_params:
                    tmp_goal = {"action_goal": "to get",
                            'object_goal': {'value': used_param, 'is_list': True}}
                    used_api.append(self.PM_goal_with_api_functions(tmp_goal, {}, api_name))
                for param_path in params_path:
                    tmp_goal = {"action_goal": "to get",
                            'object_goal': {'value': param_path, 'is_list': True}}
                    used_api.append(self.PM_goal_with_api_functions(tmp_goal, {}, api_name))

        item_res_api = {
            "api_name": api_name,
            "goal": goal,
            "method": method,
            "req_body": req_body,
            "used_api": used_api
        }
        return item_res_api

    def find_api_by_tfidf(self, text, local_goal):
        tfidf_vec = TfidfVectorizer(tokenizer=normalize_with_wordnet)

        # построим матрицу предложение-терм для нашего корпуса предложений SENTENCES
        self.arr_api_sentences.append(text)
        tfidf = tfidf_vec.fit_transform(self.arr_api_sentences)
        self.arr_api_sentences.remove(text)

        # расчёт близости вектора для запроса пользователя с векторами корпуса
        vals = cosine_similarity(tfidf[-1], tfidf)  # на выходе будет матрица 1хN

        # сортируем по убыванию косинусного расстояния, получаем матрицу индексов
        # берём единственную строку и индекс предпоследнего элемента
        # последний элемент соответствует самому вводу пользователя, который уже удалили из SENTENCES
        idx = vals.argsort()[0][-2]
        print('Лучшая мера близости корпуса: %f' % vals[0][idx])
        #50 лучших результатов
        len_result_tf = 20
        used_in_scope = (-1) * len_result_tf - 2
        best_results = [{"path_name": self.arr_api_names[vals.argsort()[0][index]], "mark": vals[0][vals.argsort()[0][index]]} for index in range(-2, used_in_scope, -1)]
        # flat = vals.flatten()   # выпрямляем матрицу в строку
        # flat.sort()
        # req_tfidf = flat[-2]    # берём предпоследнюю меру близости = vals[0][idx]

        # если мера больше порога, то выдадим найденный результат, иначе скажем "не знаю"
        if vals[0][idx] <= 0.01:
            return NOT_FOUND_API_CONST

        for result in best_results:
            path_name = result['path_name']
            if path_name in self.classifierObjects:
                classifierObject = self.classifierObjects[path_name]
                if local_goal["object_goal"]["value"] == classifierObject.object_name:
                    result["mark"] += 0.5

                if local_goal["action_goal"] == "to get":
                    if "get" in classifierObject.actions:
                        get_content = classifierObject.actions["get"]
                        if local_goal["object_goal"]["is_list"] and get_content["type_list"]:
                            result["mark"] += 0.5
                        elif local_goal["object_goal"]["value"] in classifierObject.params_path:
                            result["mark"] += 0.5
                        else:
                            result["mark"] += 0.3

                elif local_goal["action_goal"] == "to create":
                    if "post" in classifierObject.actions:
                        result["mark"] += 0.5

                elif local_goal["action_goal"] == "to put":
                    if "put" in classifierObject.actions:
                        if local_goal["object_goal"]["value"] in classifierObject.params_path:
                            result["mark"] += 0.5
                        else:
                            result["mark"] += 0.3

                elif local_goal["action_goal"] == "to delete":
                    if "delete" in classifierObject.actions:
                        if local_goal["object_goal"]["value"] in classifierObject.params_path:
                            result["mark"] += 0.5
                        else:
                            result["mark"] += 0.3

        max_mark = max([x['mark'] for x in best_results])
        res = [dict["path_name"] for dict in best_results if dict['mark'] == max_mark][0]
        return res



    # def find_api_by_tfidf(self, text):
    #     tfidf_vec = TfidfVectorizer(tokenizer=normalize_with_wordnet)
    #
    #     # построим матрицу предложение-терм для нашего корпуса предложений SENTENCES
    #     self.arr_api_sentences.append(text)
    #     tfidf = tfidf_vec.fit_transform(self.arr_api_sentences)
    #     self.arr_api_sentences.remove(text)
    #
    #     # расчёт близости вектора для запроса пользователя с векторами корпуса
    #     vals = cosine_similarity(tfidf[-1], tfidf)  # на выходе будет матрица 1хN
    #
    #     # сортируем по убыванию косинусного расстояния, получаем матрицу индексов
    #     # берём единственную строку и индекс предпоследнего элемента
    #     # последний элемент соответствует самому вводу пользователя, который уже удалили из SENTENCES
    #     idx = vals.argsort()[0][-2]
    #     print('Лучшая мера близости корпуса: %f' % vals[0][idx])
    #     #50 лучших результатов
    #     len_result_tf = 20
    #     used_in_scope = (-1) * len_result_tf - 2
    #     best_results = [{"path_name": self.arr_api_names[vals.argsort()[0][index]], "mark": vals[0][vals.argsort()[0][index]]} for index in range(-2, used_in_scope, -1)]
    #     # flat = vals.flatten()   # выпрямляем матрицу в строку
    #     # flat.sort()
    #     # req_tfidf = flat[-2]    # берём предпоследнюю меру близости = vals[0][idx]
    #
    #     # если мера больше порога, то выдадим найденный результат, иначе скажем "не знаю"
    #     for result in best_results:
    #         if result in self.classifierObjects:
    #             if
    #     if vals[0][idx] <= 0.01:
    #         return NOT_FOUND_API_CONST
    #
    #     return out