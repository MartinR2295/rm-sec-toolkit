import json
from pathlib import Path
import importlib
import sys


class RMModule(object):

    def __init__(self, root_path: Path, path: Path):
        self.root_path = root_path
        self.path = path
        self.module_meta_data = RMModuleJson.load_from_file(self.root_path.
                                                            joinpath(path).
                                                            joinpath(RMModuleJson.get_rm_module_json_file_name()))

    def get_category_path(self):
        return self.path.relative_to(self.root_path)

    # import the module and get the module class back
    def import_and_get_class(self):
        # add module folder to python path
        sys.path.append(str(self.path.absolute()))

        # import the module file and return the module class
        return importlib.import_module(self.module_meta_data.module.replace(".py", "")).get_module()


class RMModuleJson(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.version = kwargs.get("version")
        self.author = kwargs.get("author")
        self.module = kwargs.get("module")
        self.path = kwargs.get("path")
        self.short_name = kwargs.get("short-name")

    def save_to_file(self, path: Path):
        module_json_dict = self.__dict__
        module_json_dict.pop("path")
        with open(path.absolute(), "w") as file:
            file.write(json.dumps(module_json_dict, indent=4))

    @staticmethod
    def get_rm_module_json_file_name():
        return "rm_module.json"

    @staticmethod
    def load_from_file(path: Path):
        with open(path.absolute(), "r") as file:
            data = json.load(file)
            if type(data) is dict:
                data["path"] = path.parent
                return RMModuleJson(**data)
