import urlparse3
import re
from utils import utils
from utils.utils import replace_char
from urllib import parse
import json

class ObjectGoal:
    def __init__(self, path_json_content, complete_path_name, external_api_json):
        self.external_path_json = complete_path_name
        self.actions = {}
        self.root_parent_object_name = ""
        self.object_name = self.set_object_name(complete_path_name)
        self.parent_object_name = self.set_parent_object_name(complete_path_name)
        self.params_path = self.set_params_path(complete_path_name)
        # self.request_body_str = ""
        # self.required_param_from_req_body = []

        for name_action, value in path_json_content.items():
            self.actions[name_action] = {
                "action_content": value,
                "used_params": self.set_used_params(external_api_json, value),
                "type_list": self.actionIsList(value),
                "request_body_str": self.set_request_body(external_api_json, value)


            }
            if self.root_parent_object_name == "":
                self.root_parent_object_name = value["tags"][0]


    def actionIsList(self, value_action):
        low_summary = value_action["summary"].lower()
        return bool(re.search(".*list.*", str(low_summary)))

    def set_request_body(self, external_api_json, value_action):
        # result_list = []
        components = external_api_json["components"]
        # parameters = value_action["parameters"]
        # for parameter_dict in parameters:
        #     if "schema" in parameter_dict:
        #         if "$ref" in parameter_dict["schema"]:
        #             ref = parameter_dict["schema"]["$ref"].replace("#/components/schemas/", "")
        #             from_params = components["schemas"][ref]
        #             from_params_str = json.dumps(from_params)
        #             result_list += re.findall(r'(\w+)_id', from_params_str)
        if "requestBody" in value_action:
            requestBody = value_action["requestBody"]
            ref = requestBody['content']['application/json']['schema']["$ref"].replace("#/components/schemas/", "")
            from_request_body_str = json.dumps(components["schemas"][ref])
            return from_request_body_str

    # def get_all_req_body(self, request_body):
    #     print('$ref': '#/components/schemas/BackupJobSchema_body')
    #     # оставляем только конец пути(например /.../target -> target) и убираем остаток _query или _job
    #     string_oper = re.sub(r'\'\$ref\': \'([\w_]+)\'', r'\1\2', string_oper)

    def set_used_params(self, external_api_json, value_action):
        result_list = []
        components = external_api_json["components"]
        parameters = value_action["parameters"]
        for parameter_dict in parameters:
            if "schema" in parameter_dict:
                if "$ref" in parameter_dict["schema"]:
                    ref = parameter_dict["schema"]["$ref"].replace("#/components/schemas/", "")
                    from_params = components["schemas"][ref]
                    from_params_str = json.dumps(from_params)
                    result_list += re.findall(r'(\w+)_id', from_params_str)
        if "requestBody" in value_action:
            requestBody = value_action["requestBody"]
            # complete_request_body = self.get_all_req_body(requestBody)
            ref = requestBody['content']['application/json']['schema']["$ref"].replace("#/components/schemas/", "")
            from_request_body_str = json.dumps(components["schemas"][ref])
            # self.request_body_str = from_request_body_str
            result_list += re.findall(r'(\w+)_id', from_request_body_str)
            # if "required" in components["schemas"][ref]:
            #     required = components["schemas"][ref]['required']
            #     for value in required:
            #         self.required_param_from_req_body.append(value)
        return list(set(result_list))
        # result_used_params = list(set(result_list))
        # if self.object_name in result_used_params:
        #     result_used_params.remove(self.object_name)
        # return result_used_params

    # def set_required_param_from_req_body(self, external_api_json, value_action):
    #     if "requestBody" in value_action:
    #         requestBody = value_action["requestBody"]
    #         ref = requestBody['content']['application/json']['schema']["$ref"].replace("#/components/schemas/", "")
    #         from_request_body_str = json.dumps(components["schemas"][ref])
    #         self.request_body_str = from_request_body_str
    #         result_list += re.findall(r'\w+_id', from_request_body_str)
    #         if "required" in components["schemas"][ref]:
    #             from_request_body = components["schemas"][ref]['required']
    #             for value in required:
    #                 if (bool(re.search(".*_id", value))):
    #                     result_dict[value] = value.replace("_id", "")


    def set_params_path(self, complete_path_name):
        str_without_id = complete_path_name.replace("_id", "")
        # list_params = re.findall(r'/\{(\w+_\w+)\}', str_without_id)
        return re.findall(r'/\{(\w+_?\w+)\}', str_without_id)

    def set_object_name(self, complete_path_name):
        origin_name = replace_char(self.get_object_name(complete_path_name), "_", " ")
        # object_name = {"origin_name": origin_name,
        #                "rus_name": translate_to_rus(origin_name)}
        # return object_name
        return origin_name

    def set_parent_object_name(self, complete_path_name):
        origin_name = replace_char(self.get_parent_object_name(complete_path_name), "_", " ")
        # object_name = {"origin_name": origin_name,
        #                "rus_name": translate_to_rus(origin_name)}
        # return object_name
        return origin_name



    def get_object_name(self, path):
        # result = re.findall(r'/(\w+_?\w+)(/\{\w+_\w+\})?$', path)
        result = re.findall(r'/(\w+_?\w+)(/?|(/\{\w+_\w+\})?)$', path)
        if len(result) == 0:
            return ""
        else:
            return result[0][0]

    def get_parent_object_name(self, path):
        result = re.findall(r'/(\w+_?\w+)(/?|(/\{\w+_\w+\})?)/\w+_?\w+(/?|(/\{\w+_\w+\})?)$', path)
        if len(result) == 0:
            return ""
        else:
            return result[0][0]
