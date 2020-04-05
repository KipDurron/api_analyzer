import requests


class ApiAnalyzerRequest:

    def __init__(self, url_api_conf):
        self.url_api_conf = url_api_conf
        self.response = requests.get(self.url_api_conf, verify=False)
        self.json_response = self.response.json()
