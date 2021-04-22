import os
from .rm_module_json import RMModuleJson
import importlib


class ModuleLoader(object):

    def __init__(self):
        self.current_path = self.get_absolute_module_path()

    def append_to_current_path(self, add_part):
        self.current_path += "/{}".format(add_part)

    def get_root_path(self):
        return "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-3])

    def get_relative_module_path(self):
        return "/src/modules"

    def get_rm_module_json_file_name(self):
        return "rm_module.json"

    def get_absolute_module_path(self):
        return self.get_root_path()+self.get_relative_module_path()

    def combine_with_current_path(self, add_part):
        return self.current_path+"/"+add_part

    def is_folder_in_path_a_module(self, folder):
        return self.get_rm_module_json_file_name() in os.listdir(self.combine_with_current_path(folder))

    def get_module_json(self, folder):
        if self.is_folder_in_path_a_module(folder):
            return RMModuleJson.load_from_file(
                self.combine_with_current_path("{}/{}".format(folder,
                                                              self.get_rm_module_json_file_name())))

    def get_import_path_with_module_json(self, module_json: RMModuleJson):
        return "{}.{}".format(module_json.path.replace(self.get_root_path(), "").replace("/", ".")[1:],
                              module_json.module.replace(".py", ""))

    def import_module(self, import_path):
        return importlib.import_module(import_path).get_module()

