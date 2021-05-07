import os
from .rm_module_json import RMModuleJson
import importlib
from ..helpers.print_helper import PrintHelper

'''
Handles the actions with modules
'''


class ModuleLoader(object):

    def __init__(self):
        self.current_path = self.get_absolute_module_path()

    def append_to_current_path(self, add_part):
        self.current_path += "/{}".format(add_part)

    def navigate_back(self):
        if not self.current_path_is_root_path():
            self.current_path = "/".join(self.current_path.split("/")[:-1])

    # get the path of the root path of the script itself (the folder where rm-sec-toolkit.py is located
    def get_root_path(self):
        return "/usr/local/share/rm-sec-toolkit"

    # get the path where the modules are located in the root folder
    def get_relative_module_path(self):
        return "/modules"

    # get the name of the module json file
    def get_rm_module_json_file_name(self):
        return "rm_module.json"

    # get the name of the category json file
    def get_rm_category_json_file_name(self):
        return "rm_category.json"

    # get the absolute path to the module path
    def get_absolute_module_path(self):
        return self.get_root_path() + self.get_relative_module_path()

    # combines the current path with another path (but don't append it)
    def combine_with_current_path(self, add_part):
        return self.current_path + (lambda: "" if add_part.startswith("/") else "/")() + add_part

    # check if a folder in the current path is a module
    # it simply checks if the module json exists
    def is_folder_in_path_a_module(self, folder):
        path = self.combine_with_current_path(folder)
        return os.path.isdir(path) and self.get_rm_module_json_file_name() in os.listdir(path)

    # check if a folder in the current path is a category
    # it simply checks if the category json exists
    def is_folder_in_path_a_category(self, folder):
        path = self.combine_with_current_path(folder)
        return os.path.isdir(path) and self.get_rm_category_json_file_name() in os.listdir(path)

    # load the modue json file as RMModuleJson object
    def get_module_json(self, folder):
        if self.is_folder_in_path_a_module(folder):
            return RMModuleJson.load_from_file(
                self.combine_with_current_path("{}/{}".format(folder,
                                                              self.get_rm_module_json_file_name())))

    # get the python import path from the path of a module json object
    def get_import_path_with_module_json(self, module_json: RMModuleJson):
        return "{}.{}".format(module_json.path.replace(self.get_root_path(), "").replace("/", ".")[1:],
                              module_json.module.replace(".py", ""))

    # import a module with import path and get the module from it
    def import_module(self, import_path):
        return importlib.import_module(import_path).get_module()

    # import module from folder
    def import_module_from_folder(self, folder):
        return self.import_module(self.get_import_path_with_module_json(self.get_module_json(folder)))

    # import module with a module_json object
    def import_module_with_module_json(self, module_json):
        return self.import_module(self.get_import_path_with_module_json(module_json))

    # get a list of all relevant folders (folders which are contain modules, or modules itself)
    def get_list_of_relevant_folders(self):
        return self.get_list_of_categories_of_current_path() + self.get_list_of_modules_of_current_path()

    # get a list of folders which are categories
    def get_list_of_categories_of_current_path(self):
        return [category
                for category in os.listdir(self.current_path)
                if self.is_folder_in_path_a_category(category)]

    # get a list of folders which are modules
    def get_list_of_modules_of_current_path(self):
        return [module
                for module in os.listdir(self.current_path)
                if self.is_folder_in_path_a_module(module)]

    # determine if the current path is in the root path of modules
    def current_path_is_root_path(self):
        return self.current_path == self.get_absolute_module_path()

    # show list of categories and modules, and return the selection
    # back navigations returns None
    def show_list_and_get_selection(self):
        # load categories and modules
        categories = self.get_list_of_categories_of_current_path()
        modules = self.get_list_of_modules_of_current_path()

        # print categories and modules
        print("\nContents")
        PrintHelper.print_seperator_line()
        for index, category in enumerate(categories):
            print("({}) - {} (C)".format(index + 1, category))

        for index, module in enumerate(modules):
            print("({}) - {} (M)".format(index + len(categories) + 1, module))

        # print back option if there are steps back available
        PrintHelper.print_seperator_line()
        if not self.current_path_is_root_path():
            print("(b) - back")
        print("(q) - quit")

        # get selection
        selection = None
        while selection is None:
            inp = input("\nPlease choose one element: ")

            # handle back navigation and quit
            if inp == "b" and not self.current_path_is_root_path():
                self.navigate_back()
                return None
            elif inp == "q" or inp == "quit":
                print("See you")
                exit()

            # handle the selection and return it
            if inp.isdigit():
                inp = int(inp) - 1
                if 0 <= inp < len(categories) + len(modules):
                    return (lambda: categories[inp]
                    if inp < len(categories)
                    else modules[inp - len(categories)])()

