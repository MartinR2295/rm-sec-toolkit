import json


class RMModuleJson(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.version = kwargs.get("version")
        self.author = kwargs.get("author")
        self.module = kwargs.get("module")
        self.path = kwargs.get("path")
        self.short_name = kwargs.get("short-name")

    @staticmethod
    def load_from_file(path):
        with open(path, "r") as file:
            data = json.load(file)
            if type(data) is dict:
                data["path"] = "/".join(path.split("/")[:-1])
                return RMModuleJson(**data)