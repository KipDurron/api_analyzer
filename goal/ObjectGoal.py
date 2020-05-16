import urlparse3
import re
from utils import utils
from utils.utils import replace_char, translate_to_rus
from urllib import parse


class ObjectGoal:
    def __init__(self, path_json_content, complete_path_name, components):
        self.external_path_json = complete_path_name
        self.actions = {}
        self.root_parent_object_name = ""
        self.object_name = self.set_object_name(complete_path_name)
        self.parent_object_name = self.set_parent_object_name(complete_path_name)
        self.params_path = self.set_params_path(complete_path_name)

        for name_action, value in path_json_content.items():
            self.actions[name_action] = {
                "action_content": value,

            }
            if self.root_parent_object_name == "":
                self.root_parent_object_name = value["tags"][0]




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
