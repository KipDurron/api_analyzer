from goal.ObjectGoal import ObjectGoal


class ClassifierObjects:
    def __init__(self, external_api_json):
        self.external_api_json = external_api_json
        self.classifierObjects = self.classifier()
        # self.norm_class_objects = self.normalase_class_objects()

    def classifier(self):
        classifierObjects = {}
        for complete_path_name, path_json_content in self.external_api_json["paths"].items():
            classifierObjects[complete_path_name] = ObjectGoal(path_json_content, complete_path_name, self.external_api_json)
        return classifierObjects

    # def normalase_class_objects(self):
    #     for object in self.classifierObjects:
    #
    #